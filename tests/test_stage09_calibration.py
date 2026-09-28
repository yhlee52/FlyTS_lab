"""Blind DEC-054 calibration contracts; no public data or real calibration runs."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from flyts.stage09 import canonical_bytes
from tools.stage09_calibration import (ARMS, BASE_PATH, EVAL_PATH, METRICS, SEEDS,
                                       VIEWS, all_view_conjunction, calibration_configs,
                                       calibration_report, load_spec, synthetic_h01_fixtures,
                                       validate_pairs, validate_record_rows,
                                       run_calibration)
import tools.stage09_calibration as calibration


def _v2_fixture(tmp_path):
    output = tmp_path / "calibration"
    evidence = []
    for seed in SEEDS:
        for arm in ARMS:
            run = output / "runs" / str(seed) / arm
            raw = run / "bike_evaluation" / "records.jsonl"
            raw.parent.mkdir(parents=True)
            rows = [dict(metric="permutation", arm="perm_0", domain="transport",
                         record_id=74, window_start=1, fixture_id="p", value=0.0)]
            for window, count in ((10, 1), (20, 3)):
                baseline = (2.0 if arm == "fly_like" else 1.0) + window / 100.0
                rows.append(dict(metric="dropout", arm="0%", domain="transport",
                                 record_id=74, window_start=window, fixture_id=f"f{window}",
                                 target_count=count, baseline=baseline, value=0.0))
            raw.write_bytes(b"".join(canonical_bytes(row) for row in rows))
            fact = dict(seed=seed, arm=arm, record_count=len(rows),
                        evaluation_results=[],
                        evaluation_config_sha256=calibration.sha256(EVAL_PATH),
                        evaluation_records_sha256=calibration.sha256(raw))
            (run / "facts.json").write_bytes(canonical_bytes(fact))
            evidence.append(dict(seed=seed, arm=arm, record_count=len(rows),
                                 evaluation_results=[], facts_sha256=calibration.digest(fact)))
    original = dict(status="HOLD", exact_rules=None, claim="not tested",
                    evidence={"development_runs": evidence, "synthetic_h01": {"fixture": True}},
                    options=["review only"])
    (output / "REPORT.json").write_bytes(canonical_bytes(original))
    calibration.preserve_calibration_report_inputs(output)
    return output, calibration.sha256(output / "REPORT.json")


def test_v2_report_is_descriptive_and_byte_replays_from_raw_rows(tmp_path):
    output, original_hash = _v2_fixture(tmp_path)
    report = calibration.write_calibration_report_v2(output, original_hash)
    assert report["status"] == "HOLD" and report["exact_rules"] is None
    assert report["original_report"]["evidence"]["synthetic_h01"] == {"fixture": True}
    assert report["provenance"]["original_report_sha256"] == original_hash
    assert len(report["provenance"]["records_jsonl_sha256"]) == 6
    for item in report["clean_zero_dropout"]["per_seed"]:
        assert item["record_count"] == 1 and item["paired_zero_dropout_rows"] == 2
        assert item["masked_clean_loss"] == pytest.approx(2.175)
        assert item["temporal_only_clean_loss"] == pytest.approx(1.175)
        assert item["absolute_masked_minus_temporal"] == pytest.approx(1.0)
        assert item["relative_masked_minus_temporal"] == pytest.approx(1 / 1.175)
    assert calibration.verify_calibration_report_v2(output, original_hash) == report
    assert calibration.sha256(output / "REPORT.json") == original_hash
    with pytest.raises(ValueError, match="exists"):
        calibration.write_calibration_report_v2(output, original_hash)
    (output / "REPORT-v2.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="byte replay"):
        calibration.verify_calibration_report_v2(output, original_hash)


@pytest.mark.parametrize("change,match", [
    ("small", "small denominator"), ("nonfinite", "baseline"),
    ("identity", "identity mismatch"), ("extra", "extra seed-arm"),
    ("hash", "hash or path drift")])
def test_v2_rejects_invalid_or_drifted_source(tmp_path, change, match):
    output, original_hash = _v2_fixture(tmp_path)
    raw = output / "preserved-inputs/runs/7/temporal_only/bike_evaluation/records.jsonl"
    if change in ("small", "nonfinite", "identity"):
        rows = [json.loads(line) for line in raw.read_text().splitlines()]
        if change == "small":
            for row in rows:
                if row["metric"] == "dropout":
                    row["baseline"] = 0.0
        elif change == "nonfinite":
            rows[1]["baseline"] = float("inf")
        else:
            rows[1]["fixture_id"] = "wrong"
        raw.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
        fact_path = raw.parents[1] / "facts.json"
        fact = json.loads(fact_path.read_text())
        fact["evaluation_records_sha256"] = calibration.sha256(raw)
        fact_path.write_bytes(canonical_bytes(fact))
        original_path = output / "preserved-inputs/REPORT.json"
        original = json.loads(original_path.read_text())
        next(row for row in original["evidence"]["development_runs"]
             if row["seed"] == 7 and row["arm"] == "temporal_only")["facts_sha256"] = calibration.digest(fact)
        original_path.write_bytes(canonical_bytes(original))
        original_hash = calibration.sha256(original_path)
        files = json.loads((output / "preserved-inputs.json").read_text())
        for item in files["files"]:
            item["sha256"] = calibration.sha256(output / "preserved-inputs" / item["path"])
        (output / "preserved-inputs.json").write_bytes(canonical_bytes(files))
    elif change == "extra":
        (output / "preserved-inputs/runs/7/gru").mkdir()
    else:
        (output / "preserved-inputs/REPORT.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match=match):
        calibration.calibration_report_v2(output, original_hash)


def test_v2_rejects_missing_run_and_raw_hash_drift(tmp_path):
    output, original_hash = _v2_fixture(tmp_path)
    raw = output / "preserved-inputs/runs/7/fly_like/bike_evaluation/records.jsonl"
    raw.write_bytes(raw.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="hash or path drift"):
        calibration.calibration_report_v2(output, original_hash)
    output, original_hash = _v2_fixture(tmp_path / "other")
    (output / "preserved-inputs/runs/29/temporal_only").rename(output / "preserved-inputs/runs/29/temporal_only_missing")
    with pytest.raises(ValueError, match="missing or extra preserved input"):
        calibration.calibration_report_v2(output, original_hash)


@pytest.mark.parametrize("alias", ["07", "31", "-7", "notes"])
def test_v2_rejects_unregistered_or_noncanonical_seed_directory(tmp_path, alias):
    output, original_hash = _v2_fixture(tmp_path)
    (output / "preserved-inputs/runs" / alias).mkdir()
    with pytest.raises(ValueError, match="seed-arm"):
        calibration.calibration_report_v2(output, original_hash)


def test_v2_requires_only_exact_canonical_preserved_inputs(tmp_path, monkeypatch):
    output, original_hash = _v2_fixture(tmp_path)
    monkeypatch.setattr(calibration, "EVAL_PATH", tmp_path / "nonexistent.json")
    assert calibration.calibration_report_v2(output, original_hash)["status"] == "HOLD"
    (output / "preserved-inputs/evaluation_config.json").unlink()
    with pytest.raises(ValueError, match="missing or extra preserved input"):
        calibration.calibration_report_v2(output, original_hash)
    output, original_hash = _v2_fixture(tmp_path / "other")
    (output / "preserved-inputs/extra.json").write_text("{}")
    with pytest.raises(ValueError, match="missing or extra preserved input"):
        calibration.calibration_report_v2(output, original_hash)
    output, original_hash = _v2_fixture(tmp_path / "third")
    manifest = json.loads((output / "preserved-inputs.json").read_text())
    manifest["files"][0]["path"] = "../REPORT.json"
    (output / "preserved-inputs.json").write_bytes(canonical_bytes(manifest))
    with pytest.raises(ValueError, match="allowlist"):
        calibration.calibration_report_v2(output, original_hash)


def test_exact_six_configs_and_single_factor():
    spec = load_spec()
    assert calibration.SPEC_PATH.read_bytes() == canonical_bytes(spec)
    base = json.loads(BASE_PATH.read_text())
    rows = calibration_configs(spec, base)
    assert len(rows) == 6
    assert [(r["seed"], r["arm"]) for r in rows] == [
        (seed, arm) for seed in SEEDS for arm in ARMS]
    assert validate_pairs(rows)
    for row in rows:
        config = row["config"]
        assert config["seed"] == config["model"]["topology_seed"] == row["seed"]
        assert config["epochs"] * config["steps_per_epoch"] == 400
        assert config["batch_size"] * 400 == 3200
        assert config["threads"] == 4 and config["masking"]["temporal_ratio"] == 0.4
    changed = json.loads(json.dumps(rows))
    changed[1]["config"]["masking"]["temporal_ratio"] = 0.5
    with pytest.raises(ValueError, match="single-factor"):
        validate_pairs(changed)
    changed = json.loads(json.dumps(rows))
    changed[1]["arm"] = "gru"
    with pytest.raises(ValueError, match="six paired"):
        validate_pairs(changed)
    changed = json.loads(json.dumps(rows))
    changed[0]["config"]["steps_per_epoch"] = 201
    with pytest.raises(ValueError, match="paired|steps"):
        validate_pairs(changed)


def test_synthetic_h01_views_are_non_empirical_and_unfrozen():
    floor = json.loads(EVAL_PATH.read_text())["relative_floor"]
    result = synthetic_h01_fixtures(floor)
    assert result["status"] == "non-empirical-fixture"
    assert result["views"] == list(VIEWS)
    assert result["seen_counts"] == [11, 26]
    assert {k: v["nearest_seen"] for k, v in result["counts"].items()} == {
        "4": 11, "18": 11, "370": 26}
    assert all(v["null"]["relative"] == 0.0 and v["sensitivity"]["relative"] == 1.0
               for v in result["counts"].values())
    assert result["null_all_view_conjunction"] is True
    assert result["sensitivity_all_view_conjunction"] is False
    assert result["undefined_denominator"]["relative"] is None
    assert "threshold" in result["interpretation"]
    with pytest.raises(ValueError, match="eleven"):
        all_view_conjunction({"perm_0": True})


def test_record_rows_fail_closed_on_missing_nonfinite_or_wrong_metric(tmp_path):
    path = tmp_path / "records.jsonl"
    rows = [dict(metric=metric, arm="fixture", domain="transport", record_id=1,
                 window_start=0, value=0.0, fixture_id=f"fixture-{metric}")
            for metric in ("permutation", "dropout")]
    path.write_bytes(b"".join(canonical_bytes(row) for row in rows))
    assert len(validate_record_rows(path)) == 2
    for alteration in ({"value": float("nan")}, {"value": None}, {"metric": "probe"},
                       {"domain": "energy"}, {"fixture_id": None}):
        changed = [dict(row) for row in rows]
        changed[0].update(alteration)
        path.write_text("\n".join(json.dumps(row) for row in changed) + "\n")
        with pytest.raises(ValueError, match="record"):
            validate_record_rows(path)
    path.write_bytes(canonical_bytes(rows[0]))
    with pytest.raises(ValueError, match="missing"):
        validate_record_rows(path)


def test_locked_calibration_report_is_hold_without_rules():
    synthetic = synthetic_h01_fixtures(1e-8)
    facts = [dict(seed=seed, arm=arm, optimizer_steps=400, sample_exposures=3200,
                  parameter_count=68760, record_count=2, evaluation_results=[{
                      "metric": "permutation", "domain_macro": 0.0}])
             for seed in SEEDS for arm in ARMS]
    report = calibration_report(facts, synthetic)
    assert report["status"] == "HOLD" and report["exact_rules"] is None
    assert len(report["evidence"]["development_runs"]) == 6
    assert canonical_bytes(report) == canonical_bytes(calibration_report(facts, synthetic))
    facts[0]["parameter_count"] = 1
    with pytest.raises(ValueError, match="incomplete"):
        calibration_report(facts, synthetic)


def test_runner_invocation_is_cpu_development_only_and_output_is_new(tmp_path, monkeypatch):
    calls = []
    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=0, stdout=b"fixture", stderr=b"")
    monkeypatch.setattr(calibration.subprocess, "run", fake_run)
    output = tmp_path / "run"
    argv = calibration._run_segment(tmp_path / "manifest.json", tmp_path / "registry.json",
                                     tmp_path / "config.json", output, 1)
    assert argv == calls[0][0]
    assert "--development-only" in argv and argv[argv.index("--device")+1] == "cpu"
    assert argv[argv.index("--epochs")+1] == "1"
    assert (output / "segment_1.log").is_file()
    with pytest.raises(ValueError, match="output exists"):
        run_calibration(tmp_path / "missing", tmp_path / "missing-registry", output)
    with pytest.raises(ValueError, match="ignored outputs"):
        run_calibration(tmp_path / "missing", tmp_path / "missing-registry", tmp_path / "new")
