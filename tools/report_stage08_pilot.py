"""Byte-stable descriptive Stage 08 report from verified local run artifacts."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from flyts.corpus import sha256

ORDER = ("fly_like", "degree_preserving_rewired", "random_sparse", "gru", "dense_leaky")
STAGE08_METRICS = ["channel_count", "dropout", "permutation", "reconstruction"]


def canonical_digest(value):
    body = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


def current_package_hashes(spec):
    config_dir = ROOT / "configs" / "pilot" / "stage08"
    return {"pilot_manifest_sha256": sha256(config_dir / "manifest.json"),
            "pilot_config_sha256": {f"configs/pilot/stage08/{arm}.json": sha256(config_dir / f"{arm}.json")
                                    for arm in spec["core_order"] + spec["diagnostic_order"]},
            "approved_reference_config_sha256": {name: sha256(ROOT / name) for name in
                                                 ("configs/baselines/stage07-budget.json",
                                                  "configs/topology/stage05-controls.json")},
            "tool_sha256": {f"tools/{name}": sha256(ROOT / "tools" / name)
                            for name in ("run_stage08_pilot.py", "report_stage08_pilot.py")},
            "source_sha256": {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
                              for path in sorted((ROOT / "src" / "flyts").rglob("*.py"))},
            "evaluation_config_sha256": sha256(ROOT / spec["evaluation_config"])}


def checkpoint_steps(state):
    values = [entry["step"].item() for entry in state["optimizer"]["state"].values()
              if "step" in entry]
    if not values or any(not math.isfinite(value) or value != values[0] for value in values):
        raise ValueError("checkpoint optimizer step counters missing or inconsistent")
    return int(values[0])


def validate_execution(folder, facts, spec, config, resources, manifest, registry, run_config):
    arm = folder.name
    steps = config["steps_per_epoch"]
    batch_size = config["batch_size"]
    expected_parameters = spec["expected_parameters"][arm]
    expected_role = "diagnostic" if arm in spec["diagnostic_order"] else "core"
    if (type(steps) is not int or steps < 1 or type(batch_size) is not int or batch_size < 1 or
            facts.get("role") != expected_role or facts.get("steps_per_segment") != steps or
            facts.get("optimizer_steps") != 2 * steps or
            facts.get("sample_exposure") != 2 * steps * batch_size or
            facts.get("parameter_count") != expected_parameters or len(facts.get("segments", [])) != 2):
        raise ValueError(f"{arm}: execution steps, exposure or parameter facts mismatch")
    for index, (resource_path, segment) in enumerate(zip(resources, facts["segments"]), 1):
        resource = json.loads(resource_path.read_bytes())
        if resource.get("measured_steps") != steps or resource != segment["resource"]:
            raise ValueError(f"{arm}: segment measured-step mismatch")
        argv = segment.get("argv", [])
        def option(name):
            return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else None
        if (option("--epochs") != str(index) or option("--manifest") != str(manifest) or
                option("--domain-registry") != str(registry) or option("--config") != str(run_config) or
                option("--resume") != (str(folder / "pre_resume_last.pt") if index == 2 else None)):
            raise ValueError(f"{arm}: segment command or epoch boundary mismatch")
    states = [torch.load(folder / name, map_location="cpu", weights_only=True)
              for name in ("pre_resume_last.pt", "last.pt", "best.pt")]
    first, last, best = states
    histories = []
    for index, state in enumerate((first, last), 1):
        expected_config = dict(config, epochs=index)
        if (state.get("format_version") != 1 or state.get("epoch") != index or
                state.get("training_config") != expected_config or
                state.get("manifest_sha256") != facts["manifest_sha256"] or
                state.get("backbone_provenance", {}).get("parameter_count") != expected_parameters or
                checkpoint_steps(state) != index * steps or
                len(state.get("history", [])) != index):
            raise ValueError(f"{arm}: checkpoint epoch, config, optimizer or parameter mismatch")
        histories.append(state["history"])
    if histories[0] != histories[1][:1] or histories[1] != facts.get("selection_history"):
        raise ValueError(f"{arm}: segment validation history mismatch")
    losses = [row["val_loss"] for row in histories[1]]
    if any(not math.isfinite(value) for value in losses):
        raise ValueError(f"{arm}: non-finite validation history")
    earliest = losses.index(min(losses)) + 1
    if (facts.get("best_epoch") != earliest or best.get("epoch") != earliest or
            best.get("manifest_sha256") != facts["manifest_sha256"] or
            best.get("backbone_provenance", {}).get("parameter_count") != expected_parameters or
            best.get("history") != histories[1][:earliest] or
            best.get("best") != min(losses) or last.get("best") != min(losses)):
        raise ValueError(f"{arm}: earliest-best checkpoint selection mismatch")


def validate_run(folder, facts, spec):
    arm = folder.name
    if facts.get("schema_version") != 2:
        raise ValueError(f"{arm}: run facts lack exact Stage 08 provenance and phase schema")
    package = current_package_hashes(spec)
    if any(facts.get(key) != value for key, value in package.items()):
        raise ValueError(f"{arm}: approved package/tool/config/source hash mismatch")
    if facts.get("arm") != arm or arm not in spec["core_order"] + spec["diagnostic_order"]:
        raise ValueError(f"{arm}: arm identity mismatch")
    expected_role = "diagnostic" if arm in spec["diagnostic_order"] else "core"
    if facts.get("role") != expected_role:
        raise ValueError(f"{arm}: arm role mismatch")
    source_config = ROOT / "configs" / "pilot" / "stage08" / f"{arm}.json"
    if facts.get("config_source_sha256") != sha256(source_config):
        raise ValueError(f"{arm}: approved arm config hash mismatch")
    raw = source_config.read_bytes()
    config = json.loads(raw)
    if facts.get("mode") == "preflight":
        config["steps_per_epoch"] = spec["preflight_steps_per_segment"]
        expected_run_config = (json.dumps(config, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    elif facts.get("mode") == "pilot":
        expected_run_config = raw
    else:
        raise ValueError(f"{arm}: unknown mode")
    run_config = folder.parent / f"{arm}.run_config.json"
    if not run_config.exists() or run_config.read_bytes() != expected_run_config or \
            (folder / "config.json").read_bytes() != expected_run_config or \
            facts.get("run_config_sha256") != sha256(run_config):
        raise ValueError(f"{arm}: derived run config hash mismatch")
    inputs = facts.get("input_paths", {})
    manifest = Path(inputs.get("manifest", ""))
    registry = Path(inputs.get("domain_registry", ""))
    if not manifest.is_file() or not registry.is_file() or \
            sha256(manifest) != facts.get("manifest_sha256") or \
            sha256(registry) != facts.get("domain_registry_sha256") or \
            facts["manifest_sha256"] != spec["manifest_sha256"] or \
            facts["domain_registry_sha256"] != spec["domain_registry_sha256"]:
        raise ValueError(f"{arm}: frozen manifest or registry hash mismatch")
    artifacts = {"best_checkpoint_sha256": folder / "best.pt",
                 "last_checkpoint_sha256": folder / "last.pt",
                 "pre_resume_checkpoint_sha256": folder / "pre_resume_last.pt",
                 "evaluation_summary_sha256": folder / "bike_evaluation" / "summary.json",
                 "evaluation_records_sha256": folder / "bike_evaluation" / "records.jsonl"}
    if any(facts.get(key) != sha256(path) for key, path in artifacts.items()):
        raise ValueError(f"{arm}: run artifact hash mismatch")
    resources = [folder / "segment_1_resource.json", folder / "resource.json"]
    if facts.get("segment_resource_sha256") != [sha256(path) for path in resources] or \
            [json.loads(path.read_bytes()) for path in resources] != \
            [segment["resource"] for segment in facts.get("segments", [])]:
        raise ValueError(f"{arm}: process resource binding mismatch")
    validate_execution(folder, facts, spec, config, resources, manifest, registry, run_config)
    summary = json.loads(artifacts["evaluation_summary_sha256"].read_bytes())
    stable = summary["stable"]
    provenance = stable["provenance"]
    expected_provenance = {"manifest_sha256": facts["manifest_sha256"],
                           "domain_registry_sha256": facts["domain_registry_sha256"],
                           "config_sha256": package["evaluation_config_sha256"],
                           "evaluator_source_sha256": package["source_sha256"]["src/flyts/evaluation.py"],
                           "checkpoint_sha256": facts["best_checkpoint_sha256"],
                           "metric_allowlist": STAGE08_METRICS, "split": "val"}
    if any(provenance.get(key) != value for key, value in expected_provenance.items()) or \
            stable["fixture_sha256"] != facts.get("evaluation_fixture_sha256") or \
            stable["results"] != facts.get("bike_evaluator_results") or \
            provenance.get("evaluator_config") != json.loads((ROOT / spec["evaluation_config"]).read_bytes()) or \
            summary["runtime"] != facts.get("bike_evaluator_runtime"):
        raise ValueError(f"{arm}: evaluator provenance or fixture binding mismatch")
    manifest_doc = json.loads(manifest.read_bytes())
    bike_domains = {row["domain"] for row in manifest_doc["records"]
                    if row.get("domain_id", row["dataset"]) == "bike" and row["split"] == "val"}
    seen = sorted({row["shape"][1] for row in manifest_doc["records"]
                   if row["split"] == "train" and row.get("domain_id", row["dataset"]) in
                   ("appliances", "beijing")})
    if set(provenance.get("domains", [])) != bike_domains or provenance.get("seen_channel_counts") != seen:
        raise ValueError(f"{arm}: Bike domain or pretrain seen-count mismatch")
    rows = [json.loads(line) for line in artifacts["evaluation_records_sha256"].read_text(
        encoding="utf-8").splitlines()]
    if not rows or any(row["metric"] not in STAGE08_METRICS or row["domain"] not in bike_domains
                       for row in rows):
        raise ValueError(f"{arm}: evaluator row scope mismatch")
    fixture_spec = {"fixture_version": "stage03-fixture-v1", "schema_version": 1,
                    "config": json.loads((ROOT / spec["evaluation_config"]).read_bytes()),
                    "manifest_sha256": facts["manifest_sha256"],
                    "sampled_fixture_ids": sorted(row["fixture_id"] for row in rows),
                    "metric_allowlist": STAGE08_METRICS}
    if canonical_digest(fixture_spec) != stable["fixture_sha256"]:
        raise ValueError(f"{arm}: evaluator fixture hash mismatch")


def cost_scenarios(row):
    """Descriptive five-seed linear scenarios, not a future budget decision."""
    if row["role"] != "core":
        return None
    resources = [segment["resource"] for segment in row["segments"]]
    if any(resource.get("steady_step_seconds") is None for resource in resources):
        return {str(steps): None for steps in (400, 2000, 50000)}
    steps_observed = sum(resource["measured_steps"] for resource in resources)
    steady = sum(resource["steady_step_seconds"] * resource["measured_steps"]
                 for resource in resources) / steps_observed
    setup = sum(resource["setup_seconds"] for resource in resources) + row["bike_evaluator_runtime"]["setup_seconds"]
    validation = sum(resource["validation_seconds"] for resource in resources)
    checkpoint = sum(resource["checkpoint_seconds"] for resource in resources)
    evaluation = row["bike_evaluator_runtime"]["evaluation_seconds"]
    return {str(steps): {"estimated_five_seed_seconds": 5 * (setup + steps * steady + validation + checkpoint + evaluation),
                         "per_seed": {"setup_seconds": setup,
                                      "training_step_seconds": steps * steady,
                                      "validation_seconds": validation,
                                      "checkpoint_seconds": checkpoint,
                                      "evaluation_seconds": evaluation},
                         "steady_step_seconds": steady}
            for steps in (400, 2000, 50000)}


def report_bytes(runs):
    spec = json.loads((ROOT / "configs" / "pilot" / "stage08" / "manifest.json").read_bytes())
    records = []
    for arm in ORDER:
        folder = Path(runs) / arm
        if not folder.exists():
            continue
        facts = json.loads((folder / "stage08_run.json").read_bytes())
        validate_run(folder, facts, spec)
        records.append(facts)
    if not records:
        raise ValueError("no Stage 08 runs found")
    result = {"schema_version": 1, "interpretation": "descriptive operational evidence only",
              "cost_scenario_limitations": "Linear extrapolation from one CPU run per arm. Keeps measured two-segment setup, validation and checkpoint costs, plus one Bike evaluation, fixed per seed; scales steady training-step time only. Serialization and process overhead outside measured phases may make the sum differ from wall time. Not measured five-seed cost or a Stage 09 budget decision.",
              "runs": records,
              "stage09_cost_scenarios": {row["arm"]: cost_scenarios(row) for row in records
                                          if row["role"] == "core"}}
    json_body = (json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    lines = ["# Stage 08 operational pilot", "", "Individual descriptive run values only.", "",
             "| Arm | Role | Mode | Steps | Parameters | Selected epoch | Validation loss | Bike evaluator |",
             "|---|---|---|---:|---:|---:|---:|---|"]
    for row in records:
        history = row["selection_history"]
        chosen = next(item for item in history if item["epoch"] == row["best_epoch"])
        lines.append(f"| {row['arm']} | {row['role']} | {row['mode']} | {row['optimizer_steps']} | "
                     f"{row['parameter_count']} | {row['best_epoch']} | {chosen['val_loss']:.17g} | "
                     f"{row['evaluation_summary_sha256']} |")
    lines.extend(("", "## Individual process resources", "",
                  "| Arm | Segment | Wall seconds | Setup | Training steps | Validation | Checkpoint | Steady seconds/step | Peak RSS bytes |",
                  "|---|---:|---:|---:|---:|---:|---:|---:|---:|"))
    for row in records:
        for index, segment in enumerate(row["segments"], 1):
            resource = segment["resource"]
            steady = resource["steady_step_seconds"]
            steady_text = f"{steady:.17g}" if steady is not None else "unavailable"
            lines.append(f"| {row['arm']} | {index} | {resource['wall_seconds']:.17g} | "
                         f"{resource['setup_seconds']:.17g} | {resource['training_step_seconds']:.17g} | "
                         f"{resource['validation_seconds']:.17g} | {resource['checkpoint_seconds']:.17g} | "
                         f"{steady_text} | {resource['peak_rss_bytes']} |")
    lines.extend(("", "| Arm | Bike evaluator setup | Bike evaluation | Peak RSS bytes |",
                  "|---|---:|---:|---:|"))
    for row in records:
        runtime = row["bike_evaluator_runtime"]
        lines.append(f"| {row['arm']} | {runtime['setup_seconds']:.17g} | "
                     f"{runtime['evaluation_seconds']:.17g} | {runtime['peak_rss_bytes']} |")
    lines.extend(("", "## Bike development evaluator", "",
                  "| Arm | Role | Metric | Variant | Domain macro | Micro | Worst domain | Records |",
                  "|---|---|---|---|---:|---:|---:|---:|"))
    for row in records:
        for value in row["bike_evaluator_results"]:
            fmt = lambda number: f"{number:.17g}" if number is not None else "undefined"
            lines.append(f"| {row['arm']} | {row['role']} | {value['metric']} | {value['arm']} | "
                         f"{fmt(value['domain_macro'])} | {fmt(value['micro'])} | "
                         f"{fmt(value['worst_domain'])} | {value['records']} |")
    lines.extend(("", "## Stage 09 five-seed CPU cost scenarios", "",
                  result["cost_scenario_limitations"], "",
                  "| Arm | Steps per seed | Setup/seed | Training/seed | Validation/seed | Checkpoint/seed | Evaluation/seed | Estimated five-seed seconds |",
                  "|---|---:|---:|---:|---:|---:|---:|---:|"))
    for row in records:
        scenarios = cost_scenarios(row)
        if scenarios is None:
            continue
        for steps, values in scenarios.items():
            if values is None:
                lines.append(f"| {row['arm']} | {steps} | unavailable | unavailable | unavailable | unavailable | unavailable | unavailable: no steady step after warmup |")
            else:
                phase = values["per_seed"]
                lines.append(f"| {row['arm']} | {steps} | {phase['setup_seconds']:.17g} | "
                             f"{phase['training_step_seconds']:.17g} | {phase['validation_seconds']:.17g} | "
                             f"{phase['checkpoint_seconds']:.17g} | {phase['evaluation_seconds']:.17g} | "
                             f"{values['estimated_five_seed_seconds']:.17g} |")
    return json_body, ("\n".join(lines) + "\n").encode("utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    bodies = report_bytes(args.runs)
    for path, body in zip((args.json, args.markdown), bodies):
        if args.check:
            if not path.exists() or path.read_bytes() != body:
                raise SystemExit(f"generated report differs: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)


if __name__ == "__main__":
    main()
