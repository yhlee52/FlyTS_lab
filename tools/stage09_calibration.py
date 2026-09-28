"""DEC-054 development calibration: six fixed runs, no formal/final access."""
import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from flyts.corpus import load_domain_registry, sha256
from flyts.evaluation import evaluate_robustness, nearest_seen, relative_change
from flyts.stage09 import canonical_bytes, digest, earliest_minimum
from flyts.training import load_encoder


SPEC_PATH = ROOT / "configs/calibration/stage09_dec054.json"
BASE_PATH = ROOT / "configs/pilot/stage08/fly_like.json"
EVAL_PATH = ROOT / "configs/evaluation/robustness-v1.json"
SEEDS = (7, 17, 29)
ARMS = ("fly_like", "temporal_only")
METRICS = ("permutation", "dropout", "channel_count")
VIEWS = tuple(f"perm_{i}" for i in range(8)) + tuple(f"count:{i}" for i in (4, 18, 370))
ORIGINAL_REPORT_SHA256 = "1bb8c7f9d1811ee0caceaaabbb65f146ee892e2f0e84bb88433fb5b844e5b520"


def load_spec():
    spec = json.loads(SPEC_PATH.read_text())
    required = {"protocol_version": 2, "seeds": [7, 17, 29], "graph_seeds": [7, 17, 29],
                "arms": list(ARMS), "device": "cpu", "dtype": "float32", "threads": 4,
                "batch_size": 8, "context": 256, "stride": 128, "epochs": 2,
                "steps_per_epoch": 200, "steps_per_run": 400, "exposures_per_run": 3200,
                "optimizer": {"kind": "AdamW", "lr": 0.0005, "weight_decay": 0.0001},
                "masking": {"temporal_ratio": 0.4, "channel_ratio": 0.2,
                            "channel_dropout_ratio": 0.1},
                "evaluation_split": "val", "evaluation_metrics": list(METRICS),
                "evaluation_config": "configs/evaluation/robustness-v1.json",
                "training_domains": ["appliances", "beijing"], "validation_domain": "bike",
                "expected_parameter_count": 68760, "parameter_tolerance": 0.05,
                "manifest_sha256": "44bafe48196a4afd096e387dc672cad128d390ab7e5b413ea6cbeadf5f3e7f6c",
                "registry_sha256": "0095d4cd76ad5fdaeefeccdbb4322187892cc155bfac619ca4c8618ea50b9b20"}
    if spec != required:
        raise ValueError("DEC-054 calibration scope, budget or data role drift")
    return spec


def calibration_configs(spec, base):
    expected_base = {"seed": 7, "epochs": 2, "batch_size": 8, "steps_per_epoch": 200,
                     "context": 256, "stride": 128, "threads": 4, "lr": 0.0005,
                     "masking": spec["masking"], "val_batches": 0}
    if any(base.get(key) != value for key, value in expected_base.items()) or \
            base.get("model") != {"backbone": "fly_sparse", "backend": "dense",
                                  "density": 0.1, "hidden": 128, "patch_size": 8,
                                  "populations": 16, "slots": 4, "topology": "fly_like",
                                  "topology_seed": 7, "width": 64}:
        raise ValueError("DEC-054 Stage08 reference config drift")
    rows = []
    for seed in SEEDS:
        for arm in ARMS:
            config = json.loads(json.dumps(base))
            config["seed"] = seed
            config["model"]["topology_seed"] = seed
            if arm == "temporal_only":
                config["masking"]["channel_ratio"] = 0.0
                config["masking"]["channel_dropout_ratio"] = 0.0
            rows.append({"seed": seed, "arm": arm, "config": config})
    validate_pairs(rows)
    return rows


def validate_pairs(rows):
    expected = {(seed, arm) for seed in SEEDS for arm in ARMS}
    if len(rows) != 6 or {(r.get("seed"), r.get("arm")) for r in rows} != expected:
        raise ValueError("DEC-054 requires exactly six paired seed/arm runs")
    for seed in SEEDS:
        masked, temporal = (next(r["config"] for r in rows if r["seed"] == seed and r["arm"] == arm)
                            for arm in ARMS)
        if masked["masking"] != {"temporal_ratio": 0.4, "channel_ratio": 0.2,
                                  "channel_dropout_ratio": 0.1} or \
                temporal["masking"] != {"temporal_ratio": 0.4, "channel_ratio": 0.0,
                                        "channel_dropout_ratio": 0.0}:
            raise ValueError("DEC-054 masking single-factor mismatch")
        changed = json.loads(json.dumps(temporal))
        changed["masking"] = masked["masking"]
        if changed != masked or masked["seed"] != seed or \
                masked["model"]["topology_seed"] != seed:
            raise ValueError("DEC-054 paired data/RNG/model config mismatch")
        for config in (masked, temporal):
            if any(config[key] != value for key, value in
                   (("epochs", 2), ("steps_per_epoch", 200), ("batch_size", 8),
                    ("context", 256), ("stride", 128), ("threads", 4), ("lr", 0.0005))):
                raise ValueError("DEC-054 steps/exposure/CPU contract mismatch")
    return True


def source_hashes():
    paths = sorted((ROOT / "src/flyts").rglob("*.py"))
    paths += [Path(__file__), SPEC_PATH, BASE_PATH, EVAL_PATH]
    return {path.relative_to(ROOT).as_posix(): sha256(path) for path in paths}


def validate_inputs(manifest, registry, spec):
    if sha256(manifest) != spec["manifest_sha256"] or sha256(registry) != spec["registry_sha256"]:
        raise ValueError("DEC-054 Stage06 manifest/registry hash mismatch")
    roles = load_domain_registry(manifest, registry)["roles"]
    if roles != {"appliances": "pretrain", "beijing": "pretrain",
                 "bike": "development-held-out", "electricity_raw": "final-held-out"}:
        raise ValueError("DEC-054 registered domain roles mismatch")
    return True


def all_view_conjunction(flags):
    if not isinstance(flags, dict) or set(flags) != set(VIEWS) or \
            any(type(value) is not bool for value in flags.values()):
        raise ValueError("H01 synthetic fixture needs all eleven prespecified Boolean views")
    return all(flags.values())


def synthetic_h01_fixtures(relative_floor):
    """Non-empirical count/permutation arithmetic; no effect limit is selected."""
    if type(relative_floor) not in (float, int) or not math.isfinite(relative_floor) or relative_floor <= 0:
        raise ValueError("illustrative candidate numerical floor invalid")
    seen = [11, 26]
    cases = {}
    for count in (4, 18, 370):
        near = nearest_seen(count, seen)
        cases[str(count)] = {"nearest_seen": near,
                             "kind": "interpolation" if 11 < count < 26 else "extrapolation",
                             "null": relative_change(1.0, 1.0, relative_floor),
                             "sensitivity": relative_change(2.0, 1.0, relative_floor),
                             "fixture_id": digest(["dec054-h01-synthetic-v1", count, near])}
    null_flags = {view: True for view in VIEWS}
    sensitivity_flags = dict(null_flags, **{"count:370": False})
    return {"status": "non-empirical-fixture", "interpretation": "no numerical threshold inferred",
            "seen_counts": seen, "counts": cases, "views": list(VIEWS),
            "null_all_view_conjunction": all_view_conjunction(null_flags),
            "sensitivity_all_view_conjunction": all_view_conjunction(sensitivity_flags),
            "undefined_denominator": relative_change(1.0, 0.0, relative_floor)}


def validate_record_rows(path):
    if not Path(path).is_file():
        raise ValueError("calibration evaluator record rows missing")
    rows = [json.loads(line) for line in Path(path).read_text().splitlines()]
    if not rows or {row.get("metric") for row in rows} - set(METRICS) or \
            not {"permutation", "dropout"}.issubset({row.get("metric") for row in rows}):
        raise ValueError("calibration H01/H02 record rows missing or unexpected")
    for row in rows:
        if not all(key in row for key in ("metric", "arm", "domain", "record_id",
                                          "window_start", "value", "fixture_id")) or \
                type(row["value"]) not in (int, float) or not math.isfinite(row["value"]) or \
                row["domain"] != "transport" or not row["arm"] or \
                row["record_id"] is None or type(row["window_start"]) is not int or \
                row["window_start"] < 0 or not isinstance(row["fixture_id"], str) or \
                not row["fixture_id"] or \
                ("target_count" in row and (type(row["target_count"]) is not int or row["target_count"] < 1)):
            raise ValueError("calibration record row nonfinite, missing or outside Bike")
    return rows


def _run_segment(manifest, registry, config_path, output, target_epoch, resume=None):
    command = [sys.executable, "-m", "flyts", "pretrain", "--manifest", str(manifest),
               "--domain-registry", str(registry), "--config", str(config_path),
               "--output", str(output), "--device", "cpu", "--development-only",
               "--epochs", str(target_epoch)]
    if resume is not None:
        command.extend(("--resume", str(resume)))
    environment = dict(os.environ, PYTHONPATH=str(ROOT / "src"))
    result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True)
    output.mkdir(parents=True, exist_ok=True)
    (output / f"segment_{target_epoch}.log").write_bytes(result.stdout + b"\n[stderr]\n" + result.stderr)
    if result.returncode:
        raise ValueError(f"calibration training failed at epoch {target_epoch}; inspect retained log")
    return command


def _checkpoint(path, config, manifest_hash, epoch, expected_parameters):
    model, state = load_encoder(path, device="cpu")
    parameters = sum(p.numel() for p in model.parameters())
    training = state["training_config"]
    if state["manifest_sha256"] != manifest_hash or state["epoch"] != epoch or \
            training != dict(config, epochs=epoch) or parameters != expected_parameters or \
            abs(parameters-expected_parameters)/expected_parameters > 0.05 or \
            len(state["history"]) != epoch or any(
                not math.isfinite(row["val_loss"]) or not math.isfinite(row["train_loss"])
                for row in state["history"]):
        raise ValueError("calibration checkpoint step/parameter/config/provenance mismatch")
    return state, parameters


def _run_one(row, manifest, registry, root, spec, source_at_start):
    seed, arm, config = row["seed"], row["arm"], row["config"]
    config_path = root / "configs" / f"{seed}-{arm}.json"
    run_dir = root / "runs" / str(seed) / arm
    if run_dir.exists():
        raise ValueError("calibration run output exists; rerun forbidden")
    run_dir.parent.mkdir(parents=True, exist_ok=True)
    first = _run_segment(manifest, registry, config_path, run_dir, 1)
    snapshot = run_dir / "pre_resume_last.pt"
    shutil.copy2(run_dir / "last.pt", snapshot)
    shutil.copy2(run_dir / "resource.json", run_dir / "pre_resume_resource.json")
    snapshot_hash = sha256(snapshot)
    _, parameters = _checkpoint(snapshot, config, spec["manifest_sha256"], 1,
                                spec["expected_parameter_count"])
    second = _run_segment(manifest, registry, config_path, run_dir, 2, snapshot)
    if sha256(snapshot) != snapshot_hash:
        raise ValueError("calibration pre-resume checkpoint mutated")
    last, _ = _checkpoint(run_dir / "last.pt", config, spec["manifest_sha256"], 2,
                          spec["expected_parameter_count"])
    best_epoch = earliest_minimum([item["val_loss"] for item in last["history"]])
    best, _ = _checkpoint(run_dir / "best.pt", config, spec["manifest_sha256"],
                           best_epoch, spec["expected_parameter_count"])
    if best["best"] != last["best"]:
        raise ValueError("calibration earliest-minimum selection mismatch")
    training_run = json.loads((run_dir / "run.json").read_text())
    if training_run["train_domains"] != ["energy", "environment"] or \
            training_run["manifest_sha256"] != spec["manifest_sha256"] or \
            training_run["domain_registry_sha256"] != spec["registry_sha256"] or \
            training_run["parameters"] != parameters:
        raise ValueError("calibration pretrain-domain or run provenance drift")
    from flyts.evaluation import validate_config
    if validate_config(json.loads(EVAL_PATH.read_text()))["split"] != "val":
        raise ValueError("calibration evaluator config split drift")
    evaluation = evaluate_robustness(manifest, run_dir / "best.pt", EVAL_PATH,
                                     run_dir / "bike_evaluation", device="cpu", split="val",
                                     threads=4, domain_registry=registry,
                                     allowed_domain_ids={"bike"}, metric_allowlist=METRICS)
    rows = validate_record_rows(run_dir / "bike_evaluation/records.jsonl")
    stable = evaluation["stable"]
    if stable["provenance"]["split"] != "val" or \
            stable["provenance"]["metric_allowlist"] != sorted(METRICS) or \
            stable["provenance"]["domains"] != ["transport"] or \
            any(item["metric"] not in METRICS or not math.isfinite(item["domain_macro"])
                for item in stable["results"]):
        raise ValueError("calibration evaluation metric/domain/provenance drift")
    resources = [json.loads((run_dir / path).read_text()) for path in
                 ("pre_resume_resource.json", "resource.json")]
    if any(resource["device"] != "cpu" or resource["threads"] != 4 or
           resource["dtype"] != "float32" or resource["measured_steps"] != 200
           for resource in resources):
        raise ValueError("calibration CPU/step resource mismatch")
    if source_hashes() != source_at_start or sha256(manifest) != spec["manifest_sha256"] or \
            sha256(registry) != spec["registry_sha256"]:
        raise ValueError("calibration source/data hash drift")
    facts = {"seed": seed, "arm": arm, "status": "development-only", "optimizer_steps": 400,
             "sample_exposures": 3200, "parameter_count": parameters,
             "config_sha256": sha256(config_path), "manifest_sha256": sha256(manifest),
             "registry_sha256": sha256(registry), "source_sha256": source_at_start,
             "training_run_sha256": sha256(run_dir / "run.json"),
             "pre_resume_checkpoint_sha256": snapshot_hash,
             "last_checkpoint_sha256": sha256(run_dir / "last.pt"),
             "best_checkpoint_sha256": sha256(run_dir / "best.pt"),
             "best_epoch": best_epoch, "resource_sha256": [sha256(run_dir / p) for p in
                 ("pre_resume_resource.json", "resource.json")],
             "evaluation_config_sha256": sha256(EVAL_PATH),
             "evaluation_summary_sha256": sha256(run_dir / "bike_evaluation/summary.json"),
             "evaluation_records_sha256": sha256(run_dir / "bike_evaluation/records.jsonl"),
             "record_count": len(rows), "fixture_sha256": stable["fixture_sha256"],
             "evaluation_results": stable["results"], "commands": [first, second]}
    (run_dir / "facts.json").write_bytes(canonical_bytes(facts))
    return facts


def calibration_report(facts, synthetic):
    if len(facts) != 6 or {(f.get("seed"), f.get("arm")) for f in facts} != \
            {(seed, arm) for seed in SEEDS for arm in ARMS} or \
            synthetic.get("status") != "non-empirical-fixture":
        raise ValueError("calibration report requires all six runs and synthetic fixtures")
    for fact in facts:
        if fact.get("optimizer_steps") != 400 or fact.get("sample_exposures") != 3200 or \
                fact.get("parameter_count") != 68760 or fact.get("record_count", 0) < 1:
            raise ValueError("calibration report run facts incomplete")
    return {"status": "HOLD", "protocol_version": 2,
            "evidence": {"development_runs": [{"seed": f["seed"], "arm": f["arm"],
                                                "facts_sha256": digest(f),
                                                "record_count": f["record_count"],
                                                "evaluation_results": f["evaluation_results"]}
                                               for f in sorted(facts, key=lambda f: (f["seed"], f["arm"]))],
                         "synthetic_h01": synthetic},
            "options": ["M2 review of descriptive H-01/H-02 values without freezing rules",
                        "retain HOLD where numerical/statistical evidence is insufficient"],
            "exact_rules": None, "claim": "not tested"}


def run_calibration(manifest, registry, output):
    spec = load_spec()
    manifest, registry, output = Path(manifest), Path(registry), Path(output)
    if output.exists():
        raise ValueError("calibration output exists; no overwrite or automatic rerun")
    if not output.resolve().is_relative_to((ROOT / "outputs").resolve()):
        raise ValueError("calibration output must be inside ignored outputs/")
    validate_inputs(manifest, registry, spec)
    rows = calibration_configs(spec, json.loads(BASE_PATH.read_text()))
    source_at_start = source_hashes()
    output.mkdir(parents=True, exist_ok=False)
    (output / "configs").mkdir()
    (output / "runs").mkdir()
    (output / "plan.json").write_bytes(canonical_bytes({"spec": spec, "rows": rows,
                                                          "source_sha256": source_at_start}))
    for row in rows:
        (output / "configs" / f"{row['seed']}-{row['arm']}.json").write_bytes(
            canonical_bytes(row["config"]))
    synthetic = synthetic_h01_fixtures(json.loads(EVAL_PATH.read_text())["relative_floor"])
    (output / "synthetic_h01.json").write_bytes(canonical_bytes(synthetic))
    facts = [_run_one(row, manifest, registry, output, spec, source_at_start) for row in rows]
    report = calibration_report(facts, synthetic)
    (output / "REPORT.json").write_bytes(canonical_bytes(report))
    return verify_calibration(output)


def verify_calibration(output):
    output = Path(output)
    plan = json.loads((output / "plan.json").read_text())
    spec = load_spec()
    rows = calibration_configs(spec, json.loads(BASE_PATH.read_text()))
    if plan["spec"] != spec or plan["rows"] != rows or plan["source_sha256"] != source_hashes():
        raise ValueError("calibration plan/source drift")
    synthetic = json.loads((output / "synthetic_h01.json").read_text())
    if (output / "synthetic_h01.json").read_bytes() != canonical_bytes(
            synthetic_h01_fixtures(json.loads(EVAL_PATH.read_text())["relative_floor"])):
        raise ValueError("calibration synthetic fixture replay mismatch")
    facts = []
    for row in rows:
        seed, arm = row["seed"], row["arm"]
        run = output / "runs" / str(seed) / arm
        config = output / "configs" / f"{seed}-{arm}.json"
        fact_path = run / "facts.json"
        fact = json.loads(fact_path.read_text())
        if config.read_bytes() != canonical_bytes(row["config"]) or \
                fact_path.read_bytes() != canonical_bytes(fact) or \
                fact["seed"] != seed or fact["arm"] != arm or \
                fact["config_sha256"] != sha256(config) or \
                fact["training_run_sha256"] != sha256(run / "run.json") or \
                fact["pre_resume_checkpoint_sha256"] != sha256(run / "pre_resume_last.pt") or \
                fact["last_checkpoint_sha256"] != sha256(run / "last.pt") or \
                fact["best_checkpoint_sha256"] != sha256(run / "best.pt") or \
                fact["resource_sha256"] != [sha256(run / name) for name in
                                             ("pre_resume_resource.json", "resource.json")] or \
                fact["evaluation_summary_sha256"] != sha256(run / "bike_evaluation/summary.json") or \
                fact["evaluation_records_sha256"] != sha256(run / "bike_evaluation/records.jsonl") or \
                fact["source_sha256"] != source_hashes() or \
                fact["manifest_sha256"] != spec["manifest_sha256"] or \
                fact["registry_sha256"] != spec["registry_sha256"] or \
                fact["evaluation_config_sha256"] != sha256(EVAL_PATH):
            raise ValueError("calibration run artifact replay mismatch")
        validate_record_rows(run / "bike_evaluation/records.jsonl")
        facts.append(fact)
    report = calibration_report(facts, synthetic)
    if (output / "REPORT.json").read_bytes() != canonical_bytes(report):
        raise ValueError("calibration locked report byte replay mismatch")
    return report


def _clean_record_loss(rows):
    """Target-weight windows within each Bike record, then weight records equally."""
    groups = {}
    for row in rows:
        key = (row["domain"], row["record_id"])
        groups.setdefault(key, []).append(row)
    if not groups or {key[0] for key in groups} != {"transport"} or len(groups) != 1:
        raise ValueError("calibration v2 requires exactly one Bike record")
    record_losses = []
    for group in groups.values():
        numerator = math.fsum(row["baseline"] * row["target_count"] for row in group)
        denominator = math.fsum(row["target_count"] for row in group)
        loss = numerator / denominator
        if not all(math.isfinite(value) for value in (numerator, denominator, loss)):
            raise ValueError("calibration v2 nonfinite clean loss")
        record_losses.append(loss)
    result = math.fsum(record_losses) / len(record_losses)
    if not math.isfinite(result):
        raise ValueError("calibration v2 nonfinite equal-record loss")
    return result, len(groups)


def _clean_pairs(masked, temporal, floor):
    paired = []
    for rows in (masked, temporal):
        cells = {}
        for row in rows:
            if row["metric"] != "dropout" or row["arm"] != "0%":
                continue
            if type(row.get("target_count")) is not int or row["target_count"] < 1 or \
                    type(row.get("baseline")) not in (int, float) or \
                    not math.isfinite(row["baseline"]) or \
                    type(row.get("record_id")) is not int:
                raise ValueError("calibration v2 invalid zero-dropout baseline or identity")
            key = tuple(row[field] for field in ("fixture_id", "domain", "record_id",
                                                     "window_start", "target_count"))
            if key in cells:
                raise ValueError("calibration v2 duplicate zero-dropout identity")
            cells[key] = row
        if not cells:
            raise ValueError("calibration v2 missing zero-dropout rows")
        paired.append(cells)
    if paired[0].keys() != paired[1].keys():
        raise ValueError("calibration v2 zero-dropout pair identity mismatch")
    masked_loss, masked_records = _clean_record_loss(list(paired[0].values()))
    temporal_loss, temporal_records = _clean_record_loss(list(paired[1].values()))
    if masked_records != temporal_records or abs(temporal_loss) < floor:
        raise ValueError("calibration v2 record mismatch or small denominator")
    absolute = masked_loss - temporal_loss
    relative = absolute / abs(temporal_loss)
    if not math.isfinite(absolute) or not math.isfinite(relative):
        raise ValueError("calibration v2 nonfinite clean difference")
    return {"masked_clean_loss": masked_loss, "temporal_only_clean_loss": temporal_loss,
            "absolute_masked_minus_temporal": absolute,
            "relative_masked_minus_temporal": relative,
            "record_count": masked_records, "paired_zero_dropout_rows": len(paired[0])}


def calibration_report_v2(output, expected_original_sha256=ORIGINAL_REPORT_SHA256):
    """Recompute a prospective v2 report from declared preserved inputs only."""
    output = Path(output)
    preserved = output / "preserved-inputs"
    manifest_path = output / "preserved-inputs.json"
    if not manifest_path.is_file() or manifest_path.is_symlink() or not preserved.is_dir() or preserved.is_symlink():
        raise ValueError("calibration v2 preserved input manifest missing")
    manifest = json.loads(manifest_path.read_text())
    expected_paths = {"REPORT.json", "evaluation_config.json"} | {
        f"runs/{seed}/{arm}/{name}" for seed in SEEDS for arm in ARMS
        for name in ("facts.json", "bike_evaluation/records.jsonl")}
    entries = manifest.get("files")
    if manifest.get("schema_version") != 1 or not isinstance(entries, list) or \
            {item.get("path") for item in entries if isinstance(item, dict)} != expected_paths or \
            len(entries) != len(expected_paths) or \
            [item["path"] for item in entries] != sorted(expected_paths):
        raise ValueError("calibration v2 preserved input allowlist mismatch")
    if manifest_path.read_bytes() != canonical_bytes(manifest):
        raise ValueError("calibration v2 preserved input manifest noncanonical")
    actual = {p.relative_to(preserved).as_posix() for p in preserved.rglob("*") if p.is_file() or p.is_symlink()}
    if actual != expected_paths:
        raise ValueError("calibration v2 missing or extra preserved input")
    for item in entries:
        name = item["path"]
        path = preserved / name
        if set(item) != {"path", "sha256"} or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) or \
                not path.is_file() or path.is_symlink() or \
                not path.resolve().is_relative_to(preserved.resolve()) or sha256(path) != item["sha256"]:
            raise ValueError("calibration v2 preserved input hash or path drift")
    original_path = preserved / "REPORT.json"
    if sha256(original_path) != expected_original_sha256:
        raise ValueError("calibration v2 original report hash drift")
    original = json.loads(original_path.read_text())
    expected = {(seed, arm) for seed in SEEDS for arm in ARMS}
    evidence = original.get("evidence", {}).get("development_runs", [])
    identities = [(item.get("seed"), item.get("arm")) for item in evidence]
    if len(identities) != 6 or set(identities) != expected or \
            original.get("status") != "HOLD" or original.get("exact_rules", False) is not None:
        raise ValueError("calibration v2 original report completeness or HOLD mismatch")
    runs = preserved / "runs"
    if {p.name for p in runs.iterdir() if p.is_dir()} != {str(seed) for seed in SEEDS} or \
            any(not re.fullmatch(r"0|[1-9][0-9]*", p.name) for p in runs.iterdir()) or \
            any({p.name for p in (runs / str(seed)).iterdir() if p.is_dir()} != set(ARMS)
                for seed in SEEDS) or \
            any(not p.is_dir() or p.is_symlink() for p in runs.iterdir()):
        raise ValueError("calibration v2 missing or extra seed-arm run")
    floor = json.loads((preserved / "evaluation_config.json").read_text())["relative_floor"]
    if type(floor) not in (int, float) or not math.isfinite(floor) or floor <= 0:
        raise ValueError("calibration v2 invalid existing relative floor")
    records_hashes = []
    by_seed = {}
    for seed in SEEDS:
        by_arm = {}
        for arm in ARMS:
            run = runs / str(seed) / arm
            fact_path = run / "facts.json"
            fact = json.loads(fact_path.read_text())
            row_path = run / "bike_evaluation" / "records.jsonl"
            entry = next(item for item in evidence if item["seed"] == seed and item["arm"] == arm)
            if fact_path.read_bytes() != canonical_bytes(fact) or \
                    fact.get("seed") != seed or fact.get("arm") != arm or \
                    digest(fact) != entry.get("facts_sha256") or \
                    fact.get("record_count") != entry.get("record_count") or \
                    fact.get("evaluation_results") != entry.get("evaluation_results") or \
                    fact.get("evaluation_config_sha256") != sha256(preserved / "evaluation_config.json") or \
                    fact.get("evaluation_records_sha256") != sha256(row_path):
                raise ValueError("calibration v2 original fact or raw record hash drift")
            rows = validate_record_rows(row_path)
            if len(rows) != fact["record_count"]:
                raise ValueError("calibration v2 raw record count drift")
            by_arm[arm] = rows
            records_hashes.append({"seed": seed, "arm": arm, "sha256": sha256(row_path)})
        by_seed[seed] = _clean_pairs(by_arm["fly_like"], by_arm["temporal_only"], floor)
    report = {"schema_version": 2, "status": "HOLD", "exact_rules": None,
              "claim": "not tested", "original_report": original,
              "provenance": {"original_report_sha256": expected_original_sha256,
                             "records_jsonl_sha256": records_hashes},
              "clean_zero_dropout": {
                  "interpretation": "positive masked-minus-temporal means masked clean harm",
                  "aggregation": "target-weighted within each record, then equal-record",
                  "per_seed": [{"seed": seed, **by_seed[seed]} for seed in SEEDS]}}
    if sha256(original_path) != expected_original_sha256:
        raise ValueError("calibration v2 original report changed during replay")
    for item in records_hashes:
        path = runs / str(item["seed"]) / item["arm"] / "bike_evaluation/records.jsonl"
        if sha256(path) != item["sha256"]:
            raise ValueError("calibration v2 raw record changed during replay")
    return report


def preserve_calibration_report_inputs(output, evaluation_config=EVAL_PATH):
    """Seal a new snapshot; the caller must retain the original Stage 09 evidence."""
    output = Path(output)
    preserved = output / "preserved-inputs"
    manifest_path = output / "preserved-inputs.json"
    if preserved.exists() or manifest_path.exists():
        raise ValueError("calibration v2 preserved inputs exist")
    runs = output / "runs"
    if not runs.is_dir() or {p.name for p in runs.iterdir()} != {str(seed) for seed in SEEDS} or \
            any(not p.is_dir() or p.is_symlink() or
                {child.name for child in p.iterdir()} != set(ARMS) or
                any(not child.is_dir() or child.is_symlink() for child in p.iterdir())
                for p in runs.iterdir()):
        raise ValueError("calibration v2 missing or extra seed-arm run")
    sources = {"REPORT.json": output / "REPORT.json",
               "evaluation_config.json": Path(evaluation_config)}
    for seed in SEEDS:
        for arm in ARMS:
            for name in ("facts.json", "bike_evaluation/records.jsonl"):
                relative = f"runs/{seed}/{arm}/{name}"
                sources[relative] = output / relative
    if any(not p.is_file() or p.is_symlink() for p in sources.values()):
        raise ValueError("calibration v2 source input missing")
    preserved.mkdir()
    entries = []
    for name, source in sorted(sources.items()):
        target = preserved / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        entries.append({"path": name, "sha256": sha256(target)})
    manifest_path.write_bytes(canonical_bytes({"schema_version": 1, "files": entries}))
    return manifest_path


def write_calibration_report_v2(output, expected_original_sha256=ORIGINAL_REPORT_SHA256):
    path = Path(output) / "REPORT-v2.json"
    if path.exists():
        raise ValueError("calibration v2 report exists; overwrite or rerun forbidden")
    report = calibration_report_v2(output, expected_original_sha256)
    with path.open("xb") as stream:
        stream.write(canonical_bytes(report))
    return report


def verify_calibration_report_v2(output, expected_original_sha256=ORIGINAL_REPORT_SHA256):
    report = calibration_report_v2(output, expected_original_sha256)
    if (Path(output) / "REPORT-v2.json").read_bytes() != canonical_bytes(report):
        raise ValueError("calibration v2 locked report byte replay mismatch")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--domain-registry", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="read-only byte replay of an existing run")
    mode.add_argument("--preserve-report-v2-inputs", action="store_true",
                      help="seal the exact prospective v2 reporter inputs")
    mode.add_argument("--remediate-report-v2", action="store_true",
                      help="create a prospective REPORT-v2.json from preserved inputs")
    mode.add_argument("--check-report-v2", action="store_true",
                      help="read-only prospective v2 replay from preserved inputs")
    parser.add_argument("--evaluation-config", type=Path,
                        help="config copied only while sealing v2 inputs")
    parser.add_argument("--expected-original-sha256", default=ORIGINAL_REPORT_SHA256,
                        help="externally retained REPORT.json SHA-256")
    args = parser.parse_args()
    if args.preserve_report_v2_inputs:
        if args.manifest or args.domain_registry:
            parser.error("v2 preservation must not receive manifest or domain registry")
        path = preserve_calibration_report_inputs(
            args.output, args.evaluation_config or EVAL_PATH
        )
        print(json.dumps({"status": "preserved", "manifest": str(path)}))
        return
    if args.remediate_report_v2 or args.check_report_v2:
        if args.manifest or args.domain_registry or args.evaluation_config:
            parser.error("v2 reporter must not receive live manifest, registry or config")
        report = (verify_calibration_report_v2(
            args.output, args.expected_original_sha256
        ) if args.check_report_v2 else write_calibration_report_v2(
            args.output, args.expected_original_sha256
        ))
        print(json.dumps({"status": report["status"], "runs": 6, "output": str(args.output)}))
        return
    if args.evaluation_config or args.expected_original_sha256 != ORIGINAL_REPORT_SHA256:
        parser.error("v2-only options require a v2 reporter mode")
    if args.manifest is None or args.domain_registry is None:
        parser.error("--manifest and --domain-registry are required for training or original check")
    if args.check:
        validate_inputs(args.manifest, args.domain_registry, load_spec())
    report = (verify_calibration(args.output) if args.check else
              run_calibration(args.manifest, args.domain_registry, args.output))
    print(json.dumps({"status": report["status"], "runs": 6, "output": str(args.output)}))


if __name__ == "__main__":
    main()
