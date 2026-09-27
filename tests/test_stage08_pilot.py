import json
from pathlib import Path

import pytest

from flyts.corpus import collate_windows, CorpusWriter, sha256
from flyts.evaluation import seen_channel_counts, evaluate_robustness, evaluate_window
from flyts.training import validation_losses, peak_rss_bytes, train
from tools.run_stage08_pilot import validated_config, lf_json, run_segment, selected_arms
from tools.report_stage08_pilot import report_bytes, cost_scenarios


def test_record_position_and_domain_macro_selection():
    rows = [("appliances", 1, 2.0, 1), ("appliances", 1, 18.0, 9),
            ("appliances", 2, 4.0, 1), ("beijing", 3, 8.0, 1)]
    value, domains = validation_losses(rows, {("appliances", 1), ("appliances", 2), ("beijing", 3)})
    assert domains == {"appliances": 3.0, "beijing": 8.0}
    assert value == 5.5
    with pytest.raises(ValueError, match="no masked targets"):
        validation_losses(rows, {("appliances", 1), ("appliances", 2), ("beijing", 3),
                                ("beijing", 4)})


def test_process_peak_rss_is_measured():
    assert peak_rss_bytes() > 0


def test_domain_id_batch_and_pretrain_seen_counts():
    import torch
    rows = [dict(x=torch.ones(2, 2), dt=1.0, time_known=True, label=-1,
                 dataset="bike", domain="transport", domain_id="bike", record_id=1,
                 window_start=0)]
    assert collate_windows(rows)["domain_id"] == ["bike"]
    doc = {"records": [dict(split="train", dataset="appliances", domain_id="appliances", shape=[8, 6]),
                       dict(split="train", dataset="bike", domain_id="bike", shape=[8, 20]),
                       dict(split="test", dataset="electricity_raw", domain_id="electricity_raw", shape=[8, 30])]}
    registry = {"roles": {"appliances": "pretrain", "bike": "development-held-out",
                          "electricity_raw": "final-held-out"}}
    assert seen_channel_counts(doc, registry, {"bike"}) == [6]
    with pytest.raises(ValueError, match="no pretrain"):
        seen_channel_counts({"records": doc["records"][1:]}, registry, {"bike"})


def test_final_held_out_filter_rejected_before_checkpoint_or_arrays(monkeypatch, tmp_path):
    import flyts.evaluation as evaluation
    monkeypatch.setattr(evaluation, "verify_development_corpus", lambda *a: {"records": []})
    monkeypatch.setattr(evaluation, "load_domain_registry", lambda *a: {"roles": {
        "bike": "development-held-out", "electricity_raw": "final-held-out"}})
    monkeypatch.setattr(evaluation, "load_encoder", lambda *a: pytest.fail("opened checkpoint"))
    config = Path(__file__).resolve().parents[1] / "configs/evaluation/robustness-v1.json"
    with pytest.raises(ValueError, match="development-held-out"):
        evaluate_robustness(tmp_path / "manifest.json", tmp_path / "best.pt", config,
                            tmp_path / "out", allowed_domain_ids={"electricity_raw"})
    with pytest.raises(ValueError, match="test/final"):
        evaluate_robustness(tmp_path / "manifest.json", tmp_path / "best.pt", config,
                            tmp_path / "out", split="test", allowed_domain_ids={"bike"})


def test_stage08_metric_filter_skips_padding_and_missing_execution():
    import torch
    class Adapter:
        patch_size = 4
        def encode(self, x, observed, dt, known, length, channels):
            assert x.shape[0] == 16 and x.shape[1] <= 3  # padded view must never execute
            return torch.ones(4)
        def reconstruct(self, x, observed, dt, known, length, channels, plan):
            assert x.shape[0] == 16 and x.shape[1] <= 3
            assert bool((observed == torch.isfinite(x)).all())  # added missingness must not execute
            return {"reconstruction": torch.zeros((1, *x.shape))}
    config = json.loads((Path(__file__).resolve().parents[1] /
                         "configs/evaluation/robustness-v1.json").read_text())
    config["permutation_repeats"] = config["dropout_repeats"] = 1
    sample = {"x": torch.arange(48, dtype=torch.float32).reshape(16, 3) / 48,
              "dt": 1.0, "time_known": True, "record_id": 1,
              "window_start": 0, "domain": "transport"}
    rows = evaluate_window(Adapter(), sample, config, "a" * 64, [2],
                           metric_allowlist=("reconstruction", "permutation", "dropout", "channel_count"))
    assert {row["metric"] for row in rows} == {"reconstruction", "permutation", "dropout", "channel_count"}


def test_approved_configs_and_preflight_derivation():
    spec = json.loads((Path(__file__).resolve().parents[1] /
                       "configs/pilot/stage08/manifest.json").read_text())
    for arm in spec["core_order"] + spec["diagnostic_order"]:
        path, pilot = validated_config(arm, "pilot", spec)
        _, preflight = validated_config(arm, "preflight", spec)
        assert pilot["steps_per_epoch"] == (10 if arm == "dense_leaky" else 200)
        assert preflight["steps_per_epoch"] == 1
        assert path.read_bytes() != lf_json(preflight)
    assert selected_arms("all", "preflight", spec) == spec["core_order"]
    assert selected_arms("all", "pilot", spec) == spec["core_order"] + spec["diagnostic_order"]


def test_runner_forces_real_one_then_two_epoch_process_boundary(monkeypatch, tmp_path):
    class Completed:
        returncode = 0
        stdout = b""
        stderr = b""

    commands = []
    def fake_run(command, **kwargs):
        commands.append(command)
        return Completed()

    monkeypatch.setattr("tools.run_stage08_pilot.subprocess.run", fake_run)
    common = (tmp_path / "manifest.json", tmp_path / "registry.json",
              tmp_path / "config.json", tmp_path / "output")
    run_segment(*common, target_epochs=1)
    run_segment(*common, target_epochs=2, resume=tmp_path / "epoch1.pt")
    assert commands[0][-2:] == ["--epochs", "1"]
    assert commands[1][-4:] == ["--resume", str(tmp_path / "epoch1.pt"), "--epochs", "2"]


def report_fixture(tmp_path, monkeypatch):
    import tools.report_stage08_pilot as reporter
    monkeypatch.setattr(reporter, "ROOT", tmp_path)
    def write(relative, body):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        return path
    manifest = write("corpus/manifest.json", json.dumps({"records": [
        {"dataset": "appliances", "domain_id": "appliances", "domain": "energy", "split": "train", "shape": [16, 6]},
        {"dataset": "bike", "domain_id": "bike", "domain": "transport", "split": "val", "shape": [16, 3]}]}).encode())
    registry = write("domain_roles.json", b"{}\n")
    spec = {"core_order": ["fly_like"], "diagnostic_order": [], "preflight_steps_per_segment": 1,
            "expected_parameters": {"fly_like": 68760},
            "evaluation_config": "configs/evaluation/eval.json", "manifest_sha256": sha256(manifest),
            "domain_registry_sha256": sha256(registry)}
    write("configs/pilot/stage08/manifest.json", json.dumps(spec).encode())
    write("configs/pilot/stage08/fly_like.json", b'{"epochs": 2, "batch_size": 8, "steps_per_epoch": 200}')
    write("configs/evaluation/eval.json", b"{}")
    write("configs/baselines/stage07-budget.json", b"{}")
    write("configs/topology/stage05-controls.json", b"{}")
    for relative in ("tools/run_stage08_pilot.py", "tools/report_stage08_pilot.py",
                     "src/flyts/evaluation.py", "src/flyts/training.py"):
        write(relative, relative.encode())
    folder = tmp_path / "runs" / "fly_like"
    derived_config = {"epochs": 2, "batch_size": 8, "steps_per_epoch": 1}
    derived = lf_json(derived_config)
    write("runs/fly_like/config.json", derived)
    run_config = write("runs/fly_like.run_config.json", derived)
    import torch
    history = [{"epoch": 1, "val_loss": 1.25}, {"epoch": 2, "val_loss": 1.5}]
    def checkpoint(name, epoch):
        state = {"format_version": 1, "epoch": epoch,
                 "training_config": dict(derived_config, epochs=epoch),
                 "manifest_sha256": sha256(manifest),
                 "backbone_provenance": {"parameter_count": 68760},
                 "optimizer": {"state": {0: {"step": torch.tensor(float(epoch))}}},
                 "history": history[:epoch], "best": 1.25}
        path = folder / name
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(state, path)
    checkpoint("pre_resume_last.pt", 1)
    checkpoint("last.pt", 2)
    checkpoint("best.pt", 1)
    resource = {"wall_seconds": 2.0, "setup_seconds": 0.2, "training_step_seconds": 1.0,
                "validation_seconds": 0.3, "checkpoint_seconds": 0.4,
                "steady_step_seconds": None, "measured_steps": 1, "peak_rss_bytes": 100}
    for name in ("segment_1_resource.json", "resource.json"):
        write(f"runs/fly_like/{name}", json.dumps(resource).encode())
    fixture_row = {"metric": "reconstruction", "domain": "transport", "fixture_id": "fixed"}
    write("runs/fly_like/bike_evaluation/records.jsonl", (json.dumps(fixture_row) + "\n").encode())
    fixture_hash = reporter.canonical_digest({"fixture_version": "stage03-fixture-v1", "schema_version": 1,
        "config": {}, "manifest_sha256": sha256(manifest), "sampled_fixture_ids": ["fixed"],
        "metric_allowlist": reporter.STAGE08_METRICS})
    results = [{"metric": "reconstruction", "arm": "base", "domain_macro": 0.75,
                "micro": 0.75, "worst_domain": 0.75, "records": 1}]
    runtime = {"seconds": 0.5, "setup_seconds": 0.1, "evaluation_seconds": 0.3,
               "peak_rss_bytes": 200}
    package = reporter.current_package_hashes(spec)
    provenance = {"manifest_sha256": sha256(manifest), "domain_registry_sha256": sha256(registry),
                  "config_sha256": package["evaluation_config_sha256"],
                  "evaluator_source_sha256": package["source_sha256"]["src/flyts/evaluation.py"],
                  "checkpoint_sha256": sha256(folder / "best.pt"),
                  "metric_allowlist": reporter.STAGE08_METRICS, "split": "val",
                  "domains": ["transport"], "seen_channel_counts": [6], "evaluator_config": {}}
    summary = {"stable": {"provenance": provenance, "fixture_sha256": fixture_hash,
                          "results": results}, "runtime": runtime}
    write("runs/fly_like/bike_evaluation/summary.json", json.dumps(summary).encode())
    facts = {**package, "schema_version": 2, "arm": "fly_like", "role": "core", "mode": "preflight",
             "config_source_sha256": sha256(tmp_path / "configs/pilot/stage08/fly_like.json"),
             "run_config_sha256": sha256(run_config),
             "input_paths": {"manifest": str(manifest), "domain_registry": str(registry)},
             "manifest_sha256": sha256(manifest), "domain_registry_sha256": sha256(registry),
             "best_checkpoint_sha256": sha256(folder / "best.pt"),
             "last_checkpoint_sha256": sha256(folder / "last.pt"),
             "pre_resume_checkpoint_sha256": sha256(folder / "pre_resume_last.pt"),
             "evaluation_summary_sha256": sha256(folder / "bike_evaluation/summary.json"),
             "evaluation_records_sha256": sha256(folder / "bike_evaluation/records.jsonl"),
             "evaluation_fixture_sha256": fixture_hash,
             "segment_resource_sha256": [sha256(folder / "segment_1_resource.json"), sha256(folder / "resource.json")],
             "segments": [{"resource": resource, "argv": ["python", "--manifest", str(manifest),
                            "--domain-registry", str(registry), "--config", str(run_config), "--epochs", "1"]},
                          {"resource": resource, "argv": ["python", "--manifest", str(manifest),
                            "--domain-registry", str(registry), "--config", str(run_config),
                            "--resume", str(folder / "pre_resume_last.pt"), "--epochs", "2"]}],
             "bike_evaluator_results": results, "bike_evaluator_runtime": runtime,
             "steps_per_segment": 1, "optimizer_steps": 2, "sample_exposure": 16,
             "parameter_count": 68760, "best_epoch": 1,
             "selection_history": history}
    write("runs/fly_like/stage08_run.json", json.dumps(facts).encode())
    return folder.parent, facts


def test_report_byte_stability_and_exact_binding_drift(monkeypatch, tmp_path):
    runs, facts = report_fixture(tmp_path, monkeypatch)
    assert report_bytes(runs) == report_bytes(runs)
    assert b"winner" not in report_bytes(runs)[1]
    assert b"0.75" in report_bytes(runs)[1]
    assert b"unavailable: no steady step" in report_bytes(runs)[1]
    assert cost_scenarios(facts)["400"] is None
    drift_paths = ("tools/run_stage08_pilot.py", "tools/report_stage08_pilot.py",
                   "configs/pilot/stage08/manifest.json", "configs/pilot/stage08/fly_like.json",
                   "configs/baselines/stage07-budget.json", "configs/topology/stage05-controls.json",
                   "configs/evaluation/eval.json", "src/flyts/training.py", "corpus/manifest.json",
                   "domain_roles.json", "runs/fly_like/bike_evaluation/records.jsonl",
                   "runs/fly_like/best.pt", "runs/fly_like/resource.json")
    for relative in drift_paths:
        path = tmp_path / relative
        original = path.read_bytes()
        path.write_bytes(original + b"drift")
        with pytest.raises((ValueError, json.JSONDecodeError)):
            report_bytes(runs)
        path.write_bytes(original)


def test_report_rejects_tampered_execution_facts(monkeypatch, tmp_path):
    runs, facts = report_fixture(tmp_path, monkeypatch)
    path = runs / "fly_like" / "stage08_run.json"
    for field, altered in (("optimizer_steps", 999), ("sample_exposure", 999),
                           ("parameter_count", 999), ("steps_per_segment", 999),
                           ("best_epoch", 2)):
        bad = dict(facts, **{field: altered})
        path.write_text(json.dumps(bad))
        with pytest.raises(ValueError, match="execution|selection"):
            report_bytes(runs)
    path.write_text(json.dumps(facts))
    assert report_bytes(runs) == report_bytes(runs)


def test_linear_cost_scenarios_are_five_seed_and_exclude_diagnostic():
    row = {"role": "core", "segments": [
        {"resource": {"steady_step_seconds": 2.0, "measured_steps": 200,
                      "setup_seconds": 1.0, "validation_seconds": 3.0, "checkpoint_seconds": 4.0}},
        {"resource": {"steady_step_seconds": 2.0, "measured_steps": 200,
                      "setup_seconds": 1.0, "validation_seconds": 3.0, "checkpoint_seconds": 4.0}}],
        "bike_evaluator_runtime": {"setup_seconds": 0.5, "evaluation_seconds": 2.5}}
    phases = cost_scenarios(row)["400"]["per_seed"]
    assert phases == {"setup_seconds": 2.5, "training_step_seconds": 800.0,
                      "validation_seconds": 6.0, "checkpoint_seconds": 8.0,
                      "evaluation_seconds": 2.5}
    assert cost_scenarios(row)["400"]["estimated_five_seed_seconds"] == 5 * sum(phases.values())
    assert cost_scenarios(row)["2000"]["per_seed"]["training_step_seconds"] == 4000
    assert cost_scenarios(row)["2000"]["per_seed"]["checkpoint_seconds"] == 8.0
    row["role"] = "diagnostic"
    assert cost_scenarios(row) is None


def test_training_records_separate_process_phases(tmp_path):
    import numpy as np
    writer = CorpusWriter(tmp_path / "corpus", {"fixture": "generated"})
    values = np.arange(64, dtype=np.float32).reshape(32, 2)
    writer.add(values, dataset="toy", domain="toy", split="train", group="train")
    writer.add(values, dataset="toy", domain="toy", split="val", group="val")
    manifest = writer.finish()
    config = json.loads((Path(__file__).resolve().parents[1] / "configs/stage02_smoke.json").read_text())
    config.update(epochs=1, steps_per_epoch=1, context=16, stride=16, val_batches=0)
    config["model"].update(patch_size=4, width=8, hidden=12, slots=2, populations=3)
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    out = tmp_path / "run"
    train(manifest, path, out, device="cpu")
    resource = json.loads((out / "resource.json").read_text())
    phases = [resource[key] for key in ("setup_seconds", "training_step_seconds",
                                        "validation_seconds", "checkpoint_seconds")]
    assert all(value > 0 for value in phases)
    assert sum(phases) <= resource["wall_seconds"]
    assert resource["steady_step_seconds"] is None
