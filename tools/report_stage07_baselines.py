"""Generate a deterministic, synthetic-only Stage 07 architecture report."""
import argparse
from dataclasses import replace
import difflib
import hashlib
import json
from pathlib import Path
import sys
import tempfile

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from flyts.backbones.budget import TARGET, TOLERANCE, SEARCH, ROLES, closest_match
from flyts.backbones.seeding import INIT_SCHEMA, SAMPLER_OFFSETS, SHARED_FIELDS, baseline_seed
from flyts.evaluation import FoundationAdapter
from flyts.foundation import EncoderConfig, FlyTSFoundation, reconstruction_loss
from flyts.masking import MaskPlan
from flyts.training import load_encoder, save_checkpoint


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_lf_bytes(value):
    """Serialize a generated artifact as explicit UTF-8 with LF newlines."""
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def outputs_match(outputs):
    return all(path.exists() and path.read_bytes() == body for path, body in outputs.items())


def output_mismatches(outputs):
    """Return concise diagnostics for generated artifacts that differ on disk."""
    diagnostics = []
    for path, expected in outputs.items():
        actual = path.read_bytes() if path.exists() else b""
        if actual == expected:
            continue
        relative = path.relative_to(ROOT)
        diagnostics.append(f"generated artifact differs: {relative}")
        actual_lines = actual.decode("utf-8", errors="replace").splitlines()
        expected_lines = expected.decode("utf-8", errors="replace").splitlines()
        diagnostics.extend(list(difflib.unified_diff(
            actual_lines, expected_lines, fromfile=f"tracked/{relative}",
            tofile=f"generated/{relative}", lineterm="", n=2,
        ))[:80])
    return diagnostics


def shared_hash(model):
    sha = hashlib.sha256()
    for name, tensor in model.state_dict().items():
        if name.split(".")[0] in SHARED_FIELDS:
            sha.update(name.encode() + b"\0")
            sha.update(tensor.detach().cpu().contiguous().numpy().tobytes())
    return sha.hexdigest()


def shared_equality_fingerprint(model, reference):
    """Hash a platform-neutral transcript of actual shared-tensor equality."""
    model_state = model.state_dict()
    transcript = []
    for name, expected in reference.state_dict().items():
        if name.split(".")[0] not in SHARED_FIELDS:
            continue
        actual = model_state[name]
        transcript.append({"name": name, "shape": list(expected.shape),
                           "dtype": str(expected.dtype),
                           "bitwise_equal": bool(torch.equal(actual, expected))})
    body = json.dumps(transcript, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(body).hexdigest(), all(row["bitwise_equal"] for row in transcript)


def fixed_fixture():
    x = torch.arange(2 * 19 * 3, dtype=torch.float32).reshape(2, 19, 3) / 113
    observed = torch.ones_like(x, dtype=torch.bool)
    lengths = torch.tensor([19, 13])
    temporal = torch.zeros((2, 3, 3), dtype=torch.bool)
    channel = temporal.clone()
    dropout = temporal.clone()
    temporal[:, 1] = True
    channel[:, :, 1] = True
    dropout[:, :, 2] = True
    return x, observed, lengths, MaskPlan(temporal, channel, dropout)


def step(model, optimizer, x, observed, lengths, plan):
    optimizer.zero_grad(set_to_none=True)
    out = model(x, observed, lengths=lengths, mask_plan=plan)
    reconstruction_loss(out).backward()
    gradients = all(p.grad is not None and torch.isfinite(p.grad).all()
                    for p in model.parameters())
    optimizer.step()
    return out, bool(gradients), all(torch.isfinite(p).all() for p in model.parameters())


def fixture(model):
    x, observed, lengths, plan = fixed_fixture()
    cfg = model.config
    complete = FlyTSFoundation(cfg)
    split = FlyTSFoundation(cfg)
    complete.load_state_dict(model.state_dict())
    split.load_state_dict(model.state_dict())
    opt_complete = torch.optim.AdamW(complete.parameters(), lr=1e-4)
    opt_split = torch.optim.AdamW(split.parameters(), lr=1e-4)
    out, gradients, updated = step(complete, opt_complete, x, observed, lengths, plan)
    step(complete, opt_complete, x, observed, lengths, plan)
    step(split, opt_split, x, observed, lengths, plan)
    with tempfile.TemporaryDirectory() as folder:
        checkpoint = Path(folder) / "synthetic.pt"
        save_checkpoint(checkpoint, split, opt_split, 1, {"model": {}}, "synthetic", [], 0.0)
        restored, state = load_encoder(checkpoint)
    restored.train()
    opt_restored = torch.optim.AdamW(restored.parameters(), lr=1e-4)
    opt_restored.load_state_dict(state["optimizer"])
    step(restored, opt_restored, x, observed, lengths, plan)
    exact = all(torch.equal(value, restored.state_dict()[name])
                for name, value in complete.state_dict().items())
    adapter = FoundationAdapter(restored.eval(), "synthetic")
    embedding = adapter.encode(x[0], observed[0], torch.tensor(1.0),
                               torch.tensor(1.0), 19, 3)
    reconstructed = adapter.reconstruct(x[0], observed[0], torch.tensor(1.0),
                                        torch.tensor(1.0), 19, 3,
                                        MaskPlan(plan.temporal[:1], plan.channel[:1], plan.dropout[:1]))
    padded = x.clone()
    padded[1, 13:] = 999
    with torch.no_grad():
        left = restored.encode(x, lengths=lengths)
        right = restored.encode(padded, lengths=lengths)
    public = {name: list(value.shape) for name, value in out.items() if isinstance(value, torch.Tensor)}
    return {"input_shapes": {"x": list(x.shape), "observed": list(observed.shape),
                              "lengths": list(lengths.shape),
                              "temporal_mask": list(plan.temporal.shape),
                              "channel_mask": list(plan.channel.shape),
                              "dropout_mask": list(plan.dropout.shape)},
            "public_output_shapes": public,
            "forward_finite": all(torch.isfinite(v).all() for v in out.values()
                                  if isinstance(v, torch.Tensor) and v.is_floating_point()),
            "all_gradients_finite": gradients, "update_finite": bool(updated),
            "two_step_resume_bitwise": bool(exact),
            "adapter_load_finite": bool(torch.isfinite(embedding).all()
                                        and torch.isfinite(reconstructed["reconstruction"]).all()),
            "padding_invariant": all(torch.equal(left[k], right[k]) for k in ("global", "channel")),
            "adapter_embedding_shape": list(embedding.shape),
            "adapter_reconstruction_shape": list(reconstructed["reconstruction"].shape)}


def compute(cfg, edges):
    h, s, d = cfg.hidden, cfg.slots, cfg.width
    if cfg.backbone == "gru":
        formula = "3*(slots*width*H + H*H) + H*width"
        mac = 3 * (s*d*h + h*h) + h*d
        unsupported = ["gate activations", "packing", "memory traffic"]
    else:
        formula = "H*(slots*width) + H*H + H*width"
        mac = h*s*d + h*h + h*d
        unsupported = (["edge weight assembly", "activation", "memory traffic"]
                       if cfg.backbone == "fly_sparse" else ["activation", "memory traffic"])
    return {"supported_formula": formula, "supported_mac_per_valid_patch": mac,
            "supported_flop_per_valid_patch": 2*mac, "flop_convention": "two FLOPs per MAC",
            "graph_edges": edges, "unsupported_operations": unsupported,
            "limits": "recurrent core only; excludes shared front end, biases, nonlinearities and hardware effects"}


def model_record(model, cfg, *, shared_reference, construction_rng_preserved,
                 construction_order_invariant):
    total = sum(p.numel() for p in model.parameters())
    shared = sum(p.numel() for name, p in model.named_parameters()
                 if name.split(".")[0] in SHARED_FIELDS)
    shared_equality_sha256, shared_initialization_equal = shared_equality_fingerprint(
        model, shared_reference)
    difference = total - TARGET
    edges = int(model.graph.src.numel()) if cfg.backbone == "fly_sparse" else None
    return {"kind": cfg.backbone, "role": ROLES[cfg.backbone], "selected_hidden": cfg.hidden,
            "actual_parameters": total, "target_parameters": TARGET,
            "deviation": difference, "absolute_deviation": abs(difference),
            "deviation_percent": 100*difference/TARGET,
            "within_tolerance": abs(difference) <= TARGET*TOLERANCE,
            "shared_parameters": shared, "backbone_parameters": total-shared,
            "shared_equality_sha256": shared_equality_sha256,
            "shared_initialization_equal": shared_initialization_equal,
            "construction_rng_preserved": bool(construction_rng_preserved),
            "construction_order_invariant": bool(construction_order_invariant),
            "parameter_schema": {name: list(p.shape) for name, p in model.named_parameters()},
            "fixture": fixture(model), "compute": compute(cfg, edges)}


def build_outputs():
    base = EncoderConfig()
    with torch.random.fork_rng(devices=[]):
        torch.random.default_generator.manual_seed(baseline_seed("shared-reference", base.init_seed))
        fly = FlyTSFoundation(base)
    fly_count = sum(p.numel() for p in fly.parameters())
    if fly_count != TARGET:
        raise RuntimeError(f"HOLD: canonical Fly count changed: {fly_count}")
    selected = {"fly_sparse": base}
    for kind in ("dense_leaky", "gru"):
        hidden, _ = closest_match(kind, base, FlyTSFoundation)
        selected[kind] = replace(base, backbone=kind, hidden=hidden)
    models = {"fly_sparse": fly}
    rng_check = {"fly_sparse": True}
    for kind in ("dense_leaky", "gru"):
        before = torch.get_rng_state().clone()
        models[kind] = FlyTSFoundation(selected[kind])
        rng_check[kind] = torch.equal(before, torch.get_rng_state())
    reverse = {kind: FlyTSFoundation(selected[kind]) for kind in ("gru", "dense_leaky")}
    with torch.random.fork_rng(devices=[]):
        torch.random.default_generator.manual_seed(baseline_seed("shared-reference", base.init_seed))
        fly_after_baselines = FlyTSFoundation(base)
    order_check = {"fly_sparse": shared_hash(fly) == shared_hash(fly_after_baselines)}
    for kind in reverse:
        order_check[kind] = shared_hash(models[kind]) == shared_hash(reverse[kind])
    records = {kind: model_record(models[kind], selected[kind], shared_reference=fly,
                                  construction_rng_preserved=rng_check[kind],
                                  construction_order_invariant=order_check[kind])
               for kind in ("fly_sparse", "dense_leaky", "gru")}
    hashes = {"foundation": "src/flyts/foundation.py", "training": "src/flyts/training.py",
              "evaluation": "src/flyts/evaluation.py", "base": "src/flyts/backbones/base.py",
              "backbones_init": "src/flyts/backbones/__init__.py",
              "registry": "src/flyts/backbones/registry.py",
              "fly": "src/flyts/backbones/fly_sparse.py", "dense": "src/flyts/backbones/dense_leaky.py",
              "gru": "src/flyts/backbones/gru.py", "budget": "src/flyts/backbones/budget.py",
              "seeding": "src/flyts/backbones/seeding.py", "masking": "src/flyts/masking.py",
              "topology_init": "src/flyts/topology/__init__.py",
              "topology_base": "src/flyts/topology/base.py",
              "topology_fly": "src/flyts/topology/fly_like.py",
              "topology_controls": "src/flyts/topology/controls.py",
              "topology_validation": "src/flyts/topology/validation.py",
              "topology_stats": "src/flyts/topology/stats.py",
              "report": "tools/report_stage07_baselines.py"}
    source_hashes = {name: {"path": path, "sha256": digest(ROOT / path)} for name, path in hashes.items()}
    budget = {"schema_version": 1, "target_parameters": TARGET, "tolerance_fraction": TOLERANCE,
              "search_hidden": {kind: list(bounds) for kind, bounds in SEARCH.items()},
              "tie_break": "smaller_hidden", "roles": ROLES, "fixture_schema": "stage07-synthetic-v1",
              "init_schema": INIT_SCHEMA, "shared_reference_seed": baseline_seed("shared-reference", base.init_seed),
              "shared_architecture": {"patch_size": base.patch_size, "width": base.width,
                                      "slots": base.slots, "decoder_output_per_patch": base.patch_size,
                                      "embedding_width": base.width},
              "fly_reference": {"hidden": base.hidden, "populations": base.populations,
                                "density": base.density, "topology": base.topology,
                                "topology_seed": base.topology_seed,
                                "graph_execution_backend": base.backend},
              "sampler_seed_offsets": SAMPLER_OFFSETS}
    training_template = json.loads((ROOT / "configs/cpu.json").read_text())
    config_bodies = {"stage07-budget.json": json_lf_bytes(budget)}
    for kind, name in (("fly_sparse", "fly-sparse"), ("dense_leaky", "dense-leaky"), ("gru", "gru")):
        cfg = selected[kind]
        training = dict(training_template)
        training["model"] = {"patch_size": cfg.patch_size, "width": cfg.width,
                             "slots": cfg.slots, "hidden": cfg.hidden, "backbone": kind}
        if kind == "fly_sparse":
            training["model"].update({"populations": cfg.populations, "density": cfg.density,
                                      "topology": cfg.topology, "topology_seed": cfg.topology_seed,
                                      "backend": cfg.backend})
        else:
            training["model"]["init_seed"] = cfg.init_seed
        config_bodies[f"stage07-{name}.json"] = json_lf_bytes(training)
    config_hashes = {name: hashlib.sha256(body).hexdigest() for name, body in config_bodies.items()}
    report = {"schema_version": 1, "status": "architecture-only", "fixture": "synthetic only; no corpus accessed",
              "target_parameters": TARGET, "tolerance_fraction": TOLERANCE, "init_schema": INIT_SCHEMA,
              "initialization": {"shared_namespace": "shared-reference", "backbone_namespaces": ["dense_leaky", "gru"],
                                 "shared_seed": baseline_seed("shared-reference", base.init_seed),
                                 "backbone_seeds": {kind: baseline_seed(kind, base.init_seed)
                                                    for kind in ("dense_leaky", "gru")}},
              "sampler_seed_offsets": SAMPLER_OFFSETS,
              "sampler_seeds_at_seed_7": {name: base.init_seed + offset
                                          for name, offset in SAMPLER_OFFSETS.items()},
              "source_hashes": source_hashes,
              "config_hashes": config_hashes, "models": records}
    if (not all(record["shared_initialization_equal"] for record in records.values()) or
            len({record["shared_equality_sha256"] for record in records.values()}) != 1):
        raise RuntimeError("HOLD: shared initialization mismatch")
    if not all(record["within_tolerance"] for record in records.values()):
        raise RuntimeError("HOLD: parameter budget mismatch")
    rows = ["# Stage 07 architecture baseline report", "",
            "Synthetic-only checks. No loss values, runtime or performance ranking.", "",
            "| Backbone | Role | H | Parameters | Absolute deviation | Deviation % | Within 5% | Shared equality fingerprint |",
            "|---|---|---:|---:|---:|---:|---|---|"]
    for kind in ("fly_sparse", "dense_leaky", "gru"):
        rec = records[kind]
        rows.append(f"| {kind} | {rec['role']} | {rec['selected_hidden']} | {rec['actual_parameters']} | "
                    f"{rec['absolute_deviation']} | {rec['deviation_percent']:.3f}% | "
                    f"{rec['within_tolerance']} | `{rec['shared_equality_sha256']}` |")
    rows += ["", "All three arms passed the fixed-mask synthetic forward, backward, update, "
             "checkpoint resume and adapter checks. The JSON records shapes, parameter schemas, "
             "source/config hashes and bounded compute formulas. CUDA remains unverified.", ""]
    outputs = {ROOT / "reports/baselines/stage07-baselines.json": json_lf_bytes(report),
               ROOT / "reports/baselines/stage07-baselines.md": "\n".join(rows).encode("utf-8")}
    outputs.update({ROOT / "configs/baselines" / name: body for name, body in config_bodies.items()})
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs()
    if args.check:
        if not outputs_match(outputs):
            raise SystemExit("Stage 07 generated files differ\n" +
                             "\n".join(output_mismatches(outputs)))
    else:
        for path, body in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)


if __name__ == "__main__":
    main()
