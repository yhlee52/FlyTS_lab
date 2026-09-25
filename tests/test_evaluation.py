import csv
import json
from pathlib import Path
import re
import sys

import numpy as np
import pytest
import torch

from flyts.corpus import CorpusWriter, WindowDataset, collate_windows, sha256
from flyts.evaluation import (aggregate, count_candidates, evaluate_robustness, evaluate_window,
                              fixture_seed, nearest_seen, order, relative_change,
                              representation_distance, reject_forbidden, validate_config,
                              verify_development_corpus, digest, FIXTURE_VERSION,
                              reference_stats)
from flyts.foundation import EncoderConfig, FlyTSFoundation
from flyts.masking import MaskPlan
from flyts.training import save_checkpoint, train
from tools.calibrate_robustness import bootstrap_interval, collapse_records, portable_path


CONFIG = Path(__file__).resolve().parents[1] / "configs/evaluation/robustness-v1.json"


def corpus_and_checkpoint(tmp_path):
    writer = CorpusWriter(tmp_path / "corpus", [{"name": "synthetic-test"}])
    t = np.arange(32, dtype=np.float32)
    for split, channels in (("train", 2), ("train", 4), ("val", 4), ("test", 4)):
        x = np.stack([np.sin(t/4), np.cos(t/5), t/32, np.sin(t/7)], axis=1).astype(np.float32)[:, :channels]
        writer.add(x, dataset="toy", domain="domain-a", split=split,
                   group=f"{split}-{channels}", start=0)
    manifest = writer.finish()
    torch.manual_seed(3)
    model = FlyTSFoundation(EncoderConfig(patch_size=4, width=8, hidden=12,
                                           slots=2, populations=3))
    optimizer = torch.optim.AdamW(model.parameters())
    checkpoint = tmp_path / "model.pt"
    save_checkpoint(checkpoint, model, optimizer, 1,
                    {"seed": 7, "steps_per_epoch": 4}, sha256(manifest), [], 0.0)
    return manifest, checkpoint


def test_config_role_and_test_access(tmp_path):
    config = json.loads(CONFIG.read_text())
    validate_config(config)
    config["split"] = "test"
    with pytest.raises(ValueError, match="forbids"):
        validate_config(config)
    manifest, checkpoint = corpus_and_checkpoint(tmp_path)
    with pytest.raises(ValueError, match="forbids"):
        evaluate_robustness(manifest, checkpoint, CONFIG, tmp_path / "denied", split="test")
    doc = json.loads(manifest.read_text())
    doc["records"][2]["domain_role"] = "final-held-out"
    with pytest.raises(ValueError, match="forbids"):
        reject_forbidden(doc, "val")


def test_seed_order_count_and_denominator():
    config = json.loads(CONFIG.read_text())
    a = fixture_seed(config, "a"*64, 2, 4, "dropout", 1)
    assert a == fixture_seed(config, "a"*64, 2, 4, "dropout", 1)
    assert a != fixture_seed(config, "a"*64, 2, 4, "dropout", 2)
    assert order([2, 1, 3], a) == order([3, 2, 1], a)
    assert nearest_seen(3, [2, 4]) == 2
    assert (3, "interpolation") in count_candidates([2, 4], 5)
    assert (5, "extrapolation") in count_candidates([2, 4], 5)
    assert relative_change(2.0, 0.0, 1e-8)["status"] == "undefined_small_denominator"
    assert relative_change(2.0, 0.0, 1e-8)["relative"] is None


def test_zero_norm_and_order_sensitive_control():
    assert representation_distance(torch.zeros(4), torch.ones(4), 1e-8)["status"] == "undefined_zero_norm"
    vector = torch.tensor([1.0, 2.0, 3.0])
    assert abs(representation_distance(vector, vector, 1e-8)["primary"]) < 1e-7
    assert representation_distance(vector, vector.flip(0), 1e-8)["primary"] > 0


def test_equal_record_domain_aggregation():
    rows = [dict(metric="m", arm="x", domain=d, record_id=r, window_start=w, value=v)
            for d, r, w, v in (("a", 0, 0, 0.0), ("a", 0, 1, 0.0),
                                ("a", 1, 0, 2.0), ("b", 2, 0, 10.0))]
    result = aggregate(rows)[0]
    assert result["domains"] == {"a": 1.0, "b": 10.0}
    assert result["domain_macro"] == 5.5
    assert result["micro"] == 4.0
    assert result["worst_domain"] == 10.0


def test_position_weighted_within_record_but_equal_records():
    rows = [dict(metric="reconstruction", arm="baseline", domain="a", record_id=0,
                 window_start=start, value=value, target_count=count)
            for start, value, count in ((0, 0.0, 1), (1, 10.0, 9))]
    one = aggregate(rows)[0]
    assert one["domain_macro"] == 9.0  # (0*1 + 10*9)/(1+9), not 5.0
    rows.append(dict(metric="reconstruction", arm="baseline", domain="a", record_id=1,
                     window_start=0, value=1.0, target_count=100))
    two = aggregate(rows)[0]
    assert two["domain_macro"] == 5.0  # equal records: (9+1)/2
    assert two["records"] == 2


def test_paired_position_weighting_precedes_relative_degradation():
    rows = [dict(metric="dropout", arm="30%", domain="a", record_id=0,
                 window_start=start, value=None, target_count=count,
                 baseline=1.0, corrupted=corrupt)
            for start, count, corrupt in ((0, 1, 1.0), (1, 9, 11.0))]
    result = aggregate(rows)[0]
    assert result["domain_macro"] == 9.0  # corrupted mean 10, baseline mean 1


def test_calibration_bootstrap_preserves_paired_position_counts():
    rows = [dict(metric="dropout", arm="30%", domain="a", record_id=0,
                 window_start=start, value=None, target_count=count,
                 baseline=1.0, corrupted=corrupt)
            for start, count, corrupt in ((0, 1, 1.0), (1, 9, 11.0))]
    cells = collapse_records(rows)
    assert cells[("dropout", "30%", "a", 0)] == (1.0, 10.0)
    interval = bootstrap_interval([cells, cells, cells], "dropout", "30%", resamples=100)
    assert interval["lower"] == pytest.approx(9.0)
    assert interval["upper"] == pytest.approx(9.0)
    assert interval["valid_resamples"] == 100


def test_candidate_paths_are_repo_relative(tmp_path):
    assert portable_path(CONFIG) == "configs/evaluation/robustness-v1.json"
    with pytest.raises(ValueError, match="inside the repository"):
        portable_path(tmp_path / "outside.json")


def test_window_metadata_compatible(tmp_path):
    manifest, _ = corpus_and_checkpoint(tmp_path)
    sample = WindowDataset(manifest, "val", 16, 16, 8)[0]
    batch = collate_windows([sample])
    assert batch["record_id"] == [2]
    assert batch["window_start"] == [0]
    assert batch["observed"].shape == batch["x"].shape


def test_corpus_writer_manifest_is_canonical_lf(tmp_path):
    manifest, _ = corpus_and_checkpoint(tmp_path)
    raw = manifest.read_bytes()
    assert raw.endswith(b"\n") and b"\r\n" not in raw
    assert manifest.with_suffix(".sha256").read_text().strip() == sha256(manifest)


def test_cpu_reproducible_reports_and_pairing(tmp_path):
    manifest, checkpoint = corpus_and_checkpoint(tmp_path)
    result_a = evaluate_robustness(manifest, checkpoint, CONFIG, tmp_path / "run-a")
    result_b = evaluate_robustness(manifest, checkpoint, CONFIG, tmp_path / "run-b")
    assert result_a["status"] == "candidate"
    assert result_a["stable"] == result_b["stable"]
    assert (tmp_path / "run-a/records.jsonl").read_bytes() == (tmp_path / "run-b/records.jsonl").read_bytes()
    records = [json.loads(line) for line in (tmp_path / "run-a/records.jsonl").read_text().splitlines()]
    assert records == sorted(records, key=lambda r: (r["domain"], r["record_id"], r["window_start"], r["metric"], r["arm"]))
    assert all(r["target_count"] > 0 for r in records if "target_count" in r)
    assert all(r["absolute_change"] == 0 and r["corrupted"] == r["baseline"]
               for r in records if r["metric"] == "dropout" and r["arm"] == "0%")
    assert all(r["target_count"] > 0 for r in records if r["metric"] == "missing")
    assert all(r["value"] is not None for r in records if r["metric"] == "reconstruction")
    assert all(r["status"] == "defined" for r in records if r["metric"] == "padding")
    assert all(abs(r["value"]) < 1e-6 and abs(r["shared_loss_change"]) < 1e-6
               for r in records if r["metric"] == "padding")
    assert {r["kind"] for r in records if r["metric"] == "channel_count"} == {"interpolation", "extrapolation"}
    for repeat_start in {r["window_start"] for r in records}:
        drop = [r for r in records if r["window_start"] == repeat_start and r["metric"] == "dropout"]
        assert all(len(r["removed"]) < 4 for r in drop)
    summary = result_a["stable"]["results"]
    with (tmp_path / "run-a/summary.csv").open(newline="") as stream:
        csv_rows = list(csv.DictReader(stream))
    assert len(csv_rows) == len(summary)
    assert all(float(c["domain_macro"]) == s["domain_macro"] for c, s in zip(csv_rows, summary))
    markdown = (tmp_path / "run-a/SUMMARY.md").read_text()
    assert all(f"{s['domain_macro']:.17g}" in markdown for s in summary)
    assert result_a["stable"]["provenance"]["excluded_splits"] == ["test"]
    assert result_a["runtime"]["device"] == "cpu"


def test_stage3_never_opens_test_array(tmp_path):
    manifest, checkpoint = corpus_and_checkpoint(tmp_path)
    doc = json.loads(manifest.read_text())
    (manifest.parent / doc["records"][-1]["path"]).unlink()
    result = evaluate_robustness(manifest, checkpoint, CONFIG, tmp_path / "safe")
    assert result["stable"]["provenance"]["split"] == "val"


def test_development_training_never_opens_test_array(tmp_path):
    manifest, _ = corpus_and_checkpoint(tmp_path)
    doc = json.loads(manifest.read_text())
    (manifest.parent / doc["records"][-1]["path"]).unlink()
    config = json.loads((Path(__file__).resolve().parents[1] / "configs/stage02_smoke.json").read_text())
    config.update(epochs=1, steps_per_epoch=1, context=16, stride=16, val_batches=1)
    config["model"].update(patch_size=4, width=8, hidden=12, slots=2, populations=3)
    path = tmp_path / "development-train.json"
    path.write_text(json.dumps(config))
    history = train(manifest, path, tmp_path / "train", device="cpu", development_only=True)
    assert len(history) == 1 and (tmp_path / "train/last.pt").exists()


def test_train_val_overlap_rejected_without_test_read(tmp_path):
    manifest, _ = corpus_and_checkpoint(tmp_path)
    doc = json.loads(manifest.read_text())
    doc["records"][2]["group"] = doc["records"][0]["group"]
    manifest.write_text(json.dumps(doc), encoding="utf-8")
    manifest.with_suffix(".sha256").write_text(sha256(manifest))
    (manifest.parent / doc["records"][-1]["path"]).unlink()
    with pytest.raises(ValueError, match="split overlap"):
        verify_development_corpus(manifest, "val")


def test_protocol_only_adapter(tmp_path):
    manifest, _ = corpus_and_checkpoint(tmp_path)
    sample = WindowDataset(manifest, "val", 16, 16, 8)[0]

    class DummyAdapter:
        patch_size = 4

        def encode(self, x, observed, dt, time_known, length, channel_count):
            return torch.tensor([float(torch.nan_to_num(x[:length, :channel_count]).sum()), 1.0])

        def reconstruct(self, x, observed, dt, time_known, length, channel_count, plan):
            return {"reconstruction": torch.zeros((1, *x.shape))}

        def provenance(self):
            return {"adapter": "dummy"}

    rows = evaluate_window(DummyAdapter(), sample, json.loads(CONFIG.read_text()),
                           sha256(manifest), [2, 4])
    assert rows and all("fixture_id" in row for row in rows)


def test_cli_and_result_schema(tmp_path, monkeypatch, capsys):
    manifest, checkpoint = corpus_and_checkpoint(tmp_path)
    from flyts.__main__ import main
    output = tmp_path / "cli"
    monkeypatch.setattr(sys, "argv", ["flyts", "evaluate-robustness", "--manifest", str(manifest),
                                      "--checkpoint", str(checkpoint), "--config", str(CONFIG),
                                      "--output", str(output), "--split", "val", "--device", "cpu"])
    main()
    assert json.loads(capsys.readouterr().out)["split"] == "val"
    result = json.loads((output / "summary.json").read_text())
    schema = json.loads((Path(__file__).resolve().parents[1] /
                         "schemas/robustness-result-v1.schema.json").read_text())
    assert all(field in result for field in schema["required"])
    assert result["schema_version"] == schema["properties"]["schema_version"]["const"]
    assert result["status"] == schema["properties"]["status"]["const"]
    assert all(field in result["stable"] for field in schema["properties"]["stable"]["required"])
    assert re.fullmatch(schema["properties"]["stable"]["properties"]["fixture_sha256"]["pattern"],
                        result["stable"]["fixture_sha256"])
    provenance = result["stable"]["provenance"]
    assert provenance["git_commit"] != ""
    assert provenance["evaluator_config"] == json.loads(CONFIG.read_text())
    assert provenance["checkpoint_training"]["seed"] == 7
    assert provenance["checkpoint_training"]["optimizer_steps"] == 4
    assert provenance["checkpoint_training"]["parameter_count"] > 0
    rows = [json.loads(line) for line in (output / "records.jsonl").read_text().splitlines()]
    actual_spec = {"fixture_version": FIXTURE_VERSION, "schema_version": 1,
                   "config": provenance["evaluator_config"],
                   "manifest_sha256": provenance["manifest_sha256"],
                   "sampled_fixture_ids": sorted(row["fixture_id"] for row in rows)}
    assert result["stable"]["fixture_sha256"] == digest(actual_spec)
    actual_spec["sampled_fixture_ids"][0] = "0" * 64
    assert result["stable"]["fixture_sha256"] != digest(actual_spec)


def test_missing_padding_dropout_remain_distinct():
    torch.manual_seed(0)
    model = FlyTSFoundation(EncoderConfig(patch_size=4, width=8, hidden=12,
                                           slots=2, populations=3)).eval()
    x = torch.arange(32, dtype=torch.float32).reshape(1, 16, 2)
    x[0, 0, 0] = float("nan")
    x = torch.cat([x, torch.full((1, 4, 2), float("nan"))], dim=1)
    x = torch.cat([x, torch.full((1, 20, 1), float("nan"))], dim=2)
    temporal = torch.zeros((1, 5, 3), dtype=torch.bool)
    temporal[:, 2, :] = True
    dropout = torch.zeros_like(temporal)
    dropout[:, :, 1] = True
    plan = MaskPlan(temporal, torch.zeros_like(temporal), dropout)
    with torch.no_grad():
        result = model(x, mask_plan=plan, lengths=torch.tensor([16]),
                       channel_counts=torch.tensor([2]))
    assert result["missing_mask"][0, 0, 0, 0]
    assert result["padding_mask"][0, 4].all()
    assert result["padding_mask"][0, :, 2].all()
    assert result["dropout_mask"][0, :, 1].any()
    assert not (result["target_mask"] & result["dropout_mask"]).any()
    assert not (result["missing_mask"] & result["padding_mask"]).any()


def test_shared_reference_excludes_target_and_pair_corruption():
    x = torch.tensor([[1., 10.], [2., 20.], [3., 30.], [4., 40.]])
    common_visible = torch.ones_like(x, dtype=torch.bool)
    common_visible[1, 0] = False  # Missing only in the corrupted paired view.
    common_visible[3, 1] = False  # Dropped/padded input absent from both views.
    target = torch.zeros_like(common_visible)
    target[2, 0] = True
    before = reference_stats(x, common_visible, target)
    changed = x.clone()
    changed[1, 0] = 1e9
    changed[2, 0] = -1e9
    changed[3, 1] = 1e9
    after = reference_stats(changed, common_visible, target)
    assert torch.equal(before[0], after[0])
    assert torch.equal(before[1], after[1])


def test_empty_target_and_single_channel(tmp_path):
    manifest, checkpoint = corpus_and_checkpoint(tmp_path)
    model = FlyTSFoundation(EncoderConfig(patch_size=4, width=8, hidden=12, slots=2, populations=3))
    from flyts.evaluation import FlyTSAdapter
    adapter = FlyTSAdapter(model.eval(), sha256(checkpoint))
    config = json.loads(CONFIG.read_text())
    sample = WindowDataset(manifest, "val", 16, 16, 8)[0]
    sample["x"] = sample["x"][:, :1]
    rows = evaluate_window(adapter, sample, config, sha256(manifest), [1])
    assert all(r["removed"] == [] for r in rows if r["metric"] == "dropout")
    assert not any(r["metric"] == "permutation" and r["arm"] != "identity" for r in rows)
    sample["x"] = torch.full((4, 1), float("nan"))
    with pytest.raises(ValueError, match="empty target"):
        evaluate_window(adapter, sample, config, sha256(manifest), [1])


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA device unavailable")
def test_cuda_fixture(tmp_path):
    manifest, checkpoint = corpus_and_checkpoint(tmp_path)
    result = evaluate_robustness(manifest, checkpoint, CONFIG, tmp_path / "cuda", device="cuda")
    assert result["runtime"]["device"] == "cuda:0"
