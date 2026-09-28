"""Stage 08 bounded, offline two-segment runner. Pilot execution needs a separate GO."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from flyts.corpus import load_domain_registry, sha256
from flyts.evaluation import evaluate_robustness
from flyts.training import load_encoder

CONFIG_DIR = ROOT / "configs" / "pilot" / "stage08"


def lf_json(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")


def source_hashes():
    return {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
            for path in sorted((ROOT / "src" / "flyts").rglob("*.py"))}


def approved_package_hashes(spec):
    return {"pilot_manifest_sha256": sha256(CONFIG_DIR / "manifest.json"),
            "pilot_config_sha256": {f"configs/pilot/stage08/{arm}.json": sha256(CONFIG_DIR / f"{arm}.json")
                                    for arm in spec["core_order"] + spec["diagnostic_order"]},
            "approved_reference_config_sha256": {name: sha256(ROOT / name) for name in
                                                 ("configs/baselines/stage07-budget.json",
                                                  "configs/topology/stage05-controls.json")},
            "tool_sha256": {f"tools/{name}": sha256(ROOT / "tools" / name)
                            for name in ("run_stage08_pilot.py", "report_stage08_pilot.py")},
            "source_sha256": source_hashes(),
            "evaluation_config_sha256": sha256(ROOT / spec["evaluation_config"])}


def require_inputs(manifest, registry, spec):
    if sha256(manifest) != spec["manifest_sha256"] or sha256(registry) != spec["domain_registry_sha256"]:
        raise ValueError("Stage 08 frozen manifest or registry SHA-256 mismatch")
    roles = load_domain_registry(manifest, registry)["roles"]
    if {key for key, role in roles.items() if role == "pretrain"} != {"appliances", "beijing"} or \
            {key for key, role in roles.items() if role == "development-held-out"} != {"bike"}:
        raise ValueError("Stage 08 frozen domain roles mismatch")


def validated_config(arm, mode, spec):
    path = CONFIG_DIR / f"{arm}.json"
    config = json.loads(path.read_bytes())
    diagnostic = arm in spec["diagnostic_order"]
    steps = spec["diagnostic_steps_per_segment"] if diagnostic else spec["core_steps_per_segment"]
    expected = {"seed": 7, "epochs": 2, "batch_size": 8, "steps_per_epoch": steps,
                "context": 256, "stride": 128, "threads": 4, "lr": 0.0005,
                "val_batches": 0,
                "masking": {"temporal_ratio": 0.4, "channel_ratio": 0.2,
                            "channel_dropout_ratio": 0.1}}
    if any(config.get(key) != value for key, value in expected.items()):
        raise ValueError(f"{arm}: pilot config differs from approved execution settings")
    if mode == "preflight":
        config["steps_per_epoch"] = spec["preflight_steps_per_segment"]
    return path, config


def selected_arms(arm, mode, spec):
    if arm == "all":
        return spec["core_order"] + (spec["diagnostic_order"] if mode == "pilot" else [])
    return [arm]


def check_checkpoint(path, *, epoch, steps, manifest_hash, expected_parameters, target, tolerance):
    model, state = load_encoder(path)
    parameters = sum(parameter.numel() for parameter in model.parameters())
    if state["epoch"] != epoch or state["training_config"]["steps_per_epoch"] != steps or \
            state["manifest_sha256"] != manifest_hash or parameters != expected_parameters or \
            abs(parameters - target) > target * tolerance:
        raise ValueError("Stage 08 checkpoint provenance, exposure or parameter mismatch")
    if len(state["history"]) != epoch or any(not __import__("math").isfinite(row["val_loss"])
                                                  for row in state["history"]):
        raise ValueError("Stage 08 checkpoint history incomplete or non-finite")
    minimum = min(row["val_loss"] for row in state["history"])
    if state["best"] != minimum:
        raise ValueError("checkpoint selection does not match validation minimum")
    return state, parameters


def run_segment(manifest, registry, config_path, output, *, target_epochs, resume=None):
    command = [sys.executable, "-m", "flyts", "pretrain", "--manifest", str(manifest),
               "--domain-registry", str(registry), "--config", str(config_path),
               "--output", str(output), "--device", "cpu", "--development-only"]
    if resume:
        command.extend(("--resume", str(resume)))
    # Keep the approved config at two total epochs while forcing a real process
    # boundary after epoch one. The trainer treats --epochs as a total-epoch
    # target, so the continuation advances the preserved checkpoint to epoch two.
    command.extend(("--epochs", str(target_epochs)))
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(ROOT / "src")
    completed = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True)
    output.mkdir(parents=True, exist_ok=True)
    (output / ("segment_2.log" if resume else "segment_1.log")).write_bytes(
        completed.stdout + b"\n[stderr]\n" + completed.stderr)
    if completed.returncode:
        raise RuntimeError(f"training segment failed ({completed.returncode}); see {output} logs")
    return command


def run_arm(arm, mode, manifest, registry, output, spec):
    source_config, config = validated_config(arm, mode, spec)
    package_at_start = approved_package_hashes(spec)
    source_config_hash = sha256(source_config)
    if output.exists():
        raise FileExistsError(f"run output already exists: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    # For preflight, preserve the exact derived config bytes beside its evidence.
    run_config = output.parent / f"{arm}.run_config.json"
    if run_config.exists():
        raise FileExistsError(f"run config already exists: {run_config}")
    run_config.write_bytes(lf_json(config) if mode == "preflight" else source_config.read_bytes())
    steps = config["steps_per_epoch"]
    first = run_segment(manifest, registry, run_config, output, target_epochs=1)
    (output / "config.json").write_bytes(run_config.read_bytes())
    first_resources = (output / "resource.json").read_bytes()
    (output / "segment_1_resource.json").write_bytes(first_resources)
    last = output / "last.pt"
    snapshot = output / "pre_resume_last.pt"
    shutil.copy2(last, snapshot)
    snapshot_hash = sha256(snapshot)
    _, parameters = check_checkpoint(snapshot, epoch=1, steps=steps,
        manifest_hash=spec["manifest_sha256"], expected_parameters=spec["expected_parameters"][arm],
        target=spec["parameter_target"], tolerance=spec["parameter_tolerance_fraction"])
    second = run_segment(manifest, registry, run_config, output, target_epochs=2,
                         resume=snapshot)
    if sha256(snapshot) != snapshot_hash:
        raise ValueError("pre-resume checkpoint changed during continuation")
    state_2, _ = check_checkpoint(last, epoch=2, steps=steps,
        manifest_hash=spec["manifest_sha256"], expected_parameters=parameters,
        target=spec["parameter_target"], tolerance=spec["parameter_tolerance_fraction"])
    best = output / "best.pt"
    _, best_state = load_encoder(best)
    earliest = min(state_2["history"], key=lambda row: row["val_loss"])["epoch"]
    if best_state["epoch"] != earliest or best_state["best"] != state_2["best"]:
        raise ValueError("best checkpoint must be earliest validation minimum")
    evaluation_output = output / "bike_evaluation"
    result = evaluate_robustness(manifest, best, ROOT / spec["evaluation_config"],
                                 evaluation_output, device="cpu", split="val", threads=4,
                                 domain_registry=registry, allowed_domain_ids={"bike"},
                                 metric_allowlist=("reconstruction", "permutation", "dropout", "channel_count"))
    if approved_package_hashes(spec) != package_at_start or sha256(source_config) != source_config_hash:
        raise ValueError("approved package changed during Stage 08 run")
    if sha256(manifest) != spec["manifest_sha256"] or sha256(registry) != spec["domain_registry_sha256"]:
        raise ValueError("frozen manifest or registry changed during Stage 08 run")
    facts = {"schema_version": 2, "arm": arm, "mode": mode, "role": "diagnostic" if arm in spec["diagnostic_order"] else "core",
             "config_source_sha256": source_config_hash, "run_config_sha256": sha256(run_config),
             **package_at_start, "input_paths": {"manifest": str(manifest), "domain_registry": str(registry)},
             "manifest_sha256": sha256(manifest),
             "domain_registry_sha256": sha256(registry),
             "steps_per_segment": steps, "optimizer_steps": 2 * steps, "sample_exposure": 2 * steps * config["batch_size"],
             "parameter_count": parameters, "pre_resume_checkpoint_sha256": snapshot_hash,
             "last_checkpoint_sha256": sha256(last), "best_checkpoint_sha256": sha256(best),
             "evaluation_fixture_sha256": result["stable"]["fixture_sha256"],
             "evaluation_summary_sha256": sha256(evaluation_output / "summary.json"),
             "evaluation_records_sha256": sha256(evaluation_output / "records.jsonl"),
             "segment_resource_sha256": [sha256(output / "segment_1_resource.json"),
                                         sha256(output / "resource.json")],
             "bike_evaluator_results": result["stable"]["results"],
             "bike_evaluator_runtime": result["runtime"],
             "selection_history": state_2["history"], "best_epoch": earliest,
             "segments": [{"argv": first, "resource": json.loads(first_resources)},
                          {"argv": second, "resource": json.loads((output / "resource.json").read_bytes())}]}
    (output / "stage08_run.json").write_bytes(lf_json(facts))
    return facts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--domain-registry", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=("preflight", "pilot"), default="preflight")
    parser.add_argument("--pilot-go", action="store_true", help="record separate PI pilot-run GO")
    parser.add_argument("--arm", choices=("all", "fly_like", "degree_preserving_rewired",
                                          "random_sparse", "gru", "dense_leaky"), default="all")
    args = parser.parse_args()
    if args.mode == "pilot" and not args.pilot_go:
        parser.error("pilot requires separate PI run GO and --pilot-go")
    spec = json.loads((CONFIG_DIR / "manifest.json").read_bytes())
    require_inputs(args.manifest, args.domain_registry, spec)
    arms = selected_arms(args.arm, args.mode, spec)
    for arm in arms:
        print(json.dumps(run_arm(arm, args.mode, args.manifest.resolve(),
                                 args.domain_registry.resolve(), args.output.resolve() / arm, spec),
                         sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
