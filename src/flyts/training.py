"""CPU/CUDA trainer, local checkpoints and frozen-encoder evaluation. No network."""
from dataclasses import asdict
import json
import math
import os
from pathlib import Path
import random
import subprocess
import sys
import time

import numpy as np
import torch
from torch.utils.data import DataLoader

from .corpus import (WindowDataset, collate_windows, sha256, verify_corpus,
                     verify_development_corpus, load_domain_registry)
from .foundation import EncoderConfig, FlyTSFoundation, reconstruction_loss, sample_hide
from .masking import canonical_masking, sample_mask_plan
from .topology import graph_statistics


GRAPH_BUFFER_FIELDS = ("dst", "src", "pop", "edge_type", "degree")
GRAPH_ONLY_FIELDS = ("populations", "density", "topology_seed", "backend", "topology", "topology_control_seed")
GRU_UNUSED_FIELDS = ("tau_min", "tau_max")


def validate_model_config_raw(value, *, allow_legacy_placeholders=False):
    if value.get("backbone", "fly_sparse") != "fly_sparse":
        defaults = asdict(EncoderConfig())
        for key in GRAPH_ONLY_FIELDS:
            if key in value and (not allow_legacy_placeholders or value[key] != defaults[key]):
                raise ValueError(f"{key} is graph-only for baseline backbones")
        if value["backbone"] == "gru":
            for key in GRU_UNUSED_FIELDS:
                if key in value and (not allow_legacy_placeholders or value[key] != defaults[key]):
                    raise ValueError(f"{key} is unused by GRU")


def graph_provenance(model):
    if model.config.backbone != "fly_sparse":
        raise ValueError("graph provenance applies to fly_sparse only")
    graph = model.graph.artifact
    return dict(kind=graph.kind, schema_version=graph.schema_version,
                content_hash=graph.content_hash, reference_seed=model.config.topology_seed,
                control_seed=model.config.topology_control_seed,
                resolved_seed=graph.seed, parameters=dict(graph.parameters),
                statistics=graph_statistics(graph))


def canonical_model_config(value):
    validate_model_config_raw(value, allow_legacy_placeholders=True)
    return asdict(EncoderConfig(**value))


def backbone_provenance(model):
    cfg = model.config
    result = {"kind": cfg.backbone, "schema_version": 1,
              "config": asdict(cfg),
              "hidden": cfg.hidden, "width": cfg.width, "slots": cfg.slots,
              "patch_size": cfg.patch_size, "output_width": cfg.width,
              "parameter_count": sum(p.numel() for p in model.parameters()),
              "init_schema": "legacy-fly-v1" if cfg.backbone == "fly_sparse" else "flyts-baseline-init-v1",
              "graph_execution_backend": cfg.backend if cfg.backbone == "fly_sparse" else None}
    if cfg.backbone == "fly_sparse":
        result["graph_provenance"] = graph_provenance(model)
    else:
        from .foundation import INIT_SCHEMA, baseline_seed
        result["init_schema"] = INIT_SCHEMA
        result["init_seed"] = cfg.init_seed
        if cfg.backbone == "dense_leaky":
            result["tau_min"] = cfg.tau_min
            result["tau_max"] = cfg.tau_max
        result["shared_seed"] = baseline_seed("shared-reference", cfg.init_seed)
        result["backbone_seed"] = baseline_seed(cfg.backbone, cfg.init_seed)
    return result


def require_resume_model_config(saved, requested):
    if canonical_model_config(saved) != asdict(requested):
        raise ValueError("resume requires identical model configuration")


def execution_provenance(reproduction_argv=None):
    commit = subprocess.run(["git", "rev-parse", "HEAD"],
                            cwd=Path(__file__).resolve().parents[2],
                            capture_output=True, text=True, check=False)
    return dict(source_commit=commit.stdout.strip() if commit.returncode == 0 else "unavailable",
                environment=dict(python=sys.version.split()[0], torch=str(torch.__version__),
                                 device="cpu" if not torch.cuda.is_available() else "cuda_available"),
                reproduction_argv=reproduction_argv or ["python", "-m", "flyts", "pretrain",
                                                         "--manifest", "<manifest>", "--config", "<config>",
                                                         "--output", "<output>"])


def training_reproduction_argv(manifest, config_path, output, device, *, resume=None,
                               epochs=None, development_only=False, domain_registry=None):
    argv = ["python", "-m", "flyts", "pretrain",
            "--manifest", str(manifest), "--config", str(config_path),
            "--output", str(output), "--device", str(device)]
    if resume is not None:
        argv.extend(("--resume", str(resume)))
    if epochs is not None:
        argv.extend(("--epochs", str(epochs)))
    if development_only:
        argv.append("--development-only")
    if domain_registry is not None:
        argv.extend(("--domain-registry", str(domain_registry)))
    return argv


def resolve_device(name):
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device(name)
    if device.type not in ("cpu", "cuda"):
        raise ValueError("MVP supports cpu or cuda")
    if device.type == "cuda" and not torch.cuda.is_available():
        raise ValueError("CUDA requested but unavailable; use --device cpu")
    return device


def move(batch, device):
    return {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in batch.items()}


def forward_batch(model, batch, masking, temporal_generator, channel_generator=None,
                  dropout_generator=None, validation=False):
    # Preserve the public legacy call signature and its exact temporal sampler.
    if isinstance(masking, (int, float)):
        hidden = sample_hide(batch["observed"], model.config.patch_size, masking, temporal_generator)
        return model(batch["x"], batch["observed"], batch["dt"], hide=hidden,
                     time_known=batch["time_known"], lengths=batch["lengths"],
                     channel_counts=batch.get("channel_counts"))
    if not masking.channel_ratio and not masking.channel_dropout_ratio:
        return forward_batch(model, batch, masking.temporal_ratio, temporal_generator)
    if validation:
        from dataclasses import replace
        masking = replace(masking, channel_dropout_ratio=0.0)
    plan = sample_mask_plan(batch["observed"], model.config.patch_size, masking,
                            temporal_generator, channel_generator, dropout_generator,
                            lengths=batch["lengths"])
    out = model(batch["x"], batch["observed"], batch["dt"], mask_plan=plan,
                time_known=batch["time_known"], lengths=batch["lengths"],
                channel_counts=batch.get("channel_counts"))
    if not out["target_mask"].any():
        raise ValueError("no reconstruction targets in batch; use a positive temporal_ratio when batches can be all single-channel")
    return out


def save_checkpoint(path, model, optimizer, epoch, config, manifest_hash, history, best,
                    execution=None):
    state = dict(format_version=1, model_config=asdict(model.config), model=model.state_dict(),
                 optimizer=optimizer.state_dict(), epoch=epoch, training_config=config,
                 manifest_sha256=manifest_hash, history=history, best=best,
                 torch_rng=torch.get_rng_state(),
                 cuda_rng=torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],
                 backbone_provenance=backbone_provenance(model),
                 execution_provenance=execution if execution is not None else execution_provenance())
    if model.config.backbone == "fly_sparse":
        state["graph_provenance"] = graph_provenance(model)
    temp = Path(str(path)+".tmp")
    torch.save(state, temp)
    temp.replace(path)


def load_encoder(checkpoint, device="cpu"):
    device = resolve_device(device)
    # Tensor/basic-type checkpoint only. Never deserialize arbitrary pickled models.
    state = torch.load(checkpoint, map_location="cpu", weights_only=True)
    if state.get("format_version") != 1:
        raise ValueError("unknown checkpoint version")
    validate_model_config_raw(state["model_config"], allow_legacy_placeholders=True)
    model = FlyTSFoundation(EncoderConfig(**state["model_config"]))
    expected = model.state_dict()
    if model.config.backbone == "fly_sparse":
        for field in GRAPH_BUFFER_FIELDS:
            key = f"graph.{field}"
            actual = state["model"].get(key)
            if (not isinstance(actual, torch.Tensor) or actual.dtype != expected[key].dtype
                    or actual.shape != expected[key].shape or not torch.equal(actual, expected[key])):
                raise ValueError(f"checkpoint graph buffer mismatch: {key}")
        provenance = state.get("graph_provenance")
        if provenance is None and model.config.topology != "fly_like":
            raise ValueError("control checkpoint missing graph provenance")
        if provenance is not None and provenance != graph_provenance(model):
            raise ValueError("checkpoint graph provenance mismatch")
    if state.get("backbone_provenance") is not None and state["backbone_provenance"] != backbone_provenance(model):
        raise ValueError("checkpoint backbone provenance mismatch")
    if model.config.backbone != "fly_sparse" and state.get("backbone_provenance") is None:
        raise ValueError("baseline checkpoint missing backbone provenance")
    model.load_state_dict(state["model"])
    return model.to(device).eval(), state


def validation_losses(rows, record_ids):
    """Aggregate target sums over windows, then records and dataset domains."""
    records = {}
    for domain_id, record_id, loss_sum, target_count in rows:
        if target_count < 1:
            continue
        key = (domain_id, record_id)
        total, count = records.get(key, (0.0, 0))
        records[key] = (total + loss_sum, count + target_count)
    missing = set(record_ids) - set(records)
    if missing:
        raise ValueError(f"validation records have no masked targets: {sorted(missing)}")
    domains = {}
    for (domain_id, _), (total, count) in records.items():
        domains.setdefault(domain_id, []).append(total / count)
    by_domain = {key: sum(values) / len(values) for key, values in sorted(domains.items())}
    if not by_domain:
        raise ValueError("empty validation domains")
    return sum(by_domain.values()) / len(by_domain), by_domain


def peak_rss_bytes():
    """Peak process resident set, using the native OS process counter."""
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        class Counters(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                        ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                        ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        get_process = ctypes.windll.kernel32.GetCurrentProcess
        get_process.restype = wintypes.HANDLE
        get_memory = ctypes.windll.psapi.GetProcessMemoryInfo
        get_memory.argtypes = (wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD)
        if not get_memory(get_process(), ctypes.byref(counters), counters.cb):
            raise OSError("GetProcessMemoryInfo failed")
        return int(counters.PeakWorkingSetSize)
    import resource
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(peak * (1 if sys.platform == "darwin" else 1024))


def train(manifest, config_path, output, device="auto", resume=None, epochs=None,
          development_only=False, domain_registry=None):
    process_started = time.perf_counter()
    config = json.loads(Path(config_path).read_text())
    masking = canonical_masking(config)
    if epochs is not None:
        config["epochs"] = epochs
    for key in ("epochs", "batch_size", "steps_per_epoch", "context", "stride", "threads"):
        if config[key] < 1:
            raise ValueError(f"{key} must be positive")
    if config["lr"] <= 0:
        raise ValueError("invalid learning rate")
    device = resolve_device(device)
    torch.set_num_threads(config["threads"])
    seed = config["seed"]
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if development_only:
        verify_development_corpus(manifest, "train", domain_registry)
        verify_development_corpus(manifest, "val", domain_registry)
    else:
        verify_corpus(manifest, domain_registry)
    registry = load_domain_registry(manifest, domain_registry)
    pretrain_ids = ({key for key, role in registry["roles"].items() if role == "pretrain"}
                    if registry else None)
    digest = sha256(manifest)
    validate_model_config_raw(config["model"])
    mcfg = EncoderConfig(**config["model"])
    model = FlyTSFoundation(mcfg).to(device)
    execution = execution_provenance(training_reproduction_argv(
        manifest, config_path, output, device, resume=resume, epochs=epochs,
        development_only=development_only, domain_registry=domain_registry))
    optimizer = torch.optim.AdamW(model.parameters(), lr=config["lr"], weight_decay=1e-4)
    start, history, best = 0, [], float("inf")
    if resume:
        restored, state = load_encoder(resume, device=str(device))
        if state["manifest_sha256"] != digest:
            raise ValueError("resume requires identical corpus manifest")
        require_resume_model_config(state["model_config"], mcfg)
        old = {k: v for k, v in state["training_config"].items() if k not in ("epochs", "mask_ratio", "masking")}
        new = {k: v for k, v in config.items() if k not in ("epochs", "mask_ratio", "masking")}
        old["model"] = canonical_model_config(old["model"])
        new["model"] = canonical_model_config(new["model"])
        old["masking"] = canonical_masking(state["training_config"])
        new["masking"] = masking
        if old != new:
            raise ValueError("resume may change epochs/device only; keep training config fixed")
        model.load_state_dict(restored.state_dict())
        optimizer.load_state_dict(state["optimizer"])
        start, history, best = state["epoch"], state["history"], state["best"]
        torch.set_rng_state(state["torch_rng"])
        if device.type == "cuda" and state["cuda_rng"]:
            torch.cuda.set_rng_state_all(state["cuda_rng"])
    if start >= config["epochs"]:
        raise ValueError("epochs must exceed checkpoint's completed epoch")
    outdir = Path(output)
    if not resume:
        outdir.mkdir(parents=True, exist_ok=False)
    else:
        outdir.mkdir(parents=True, exist_ok=True)
    train_data = WindowDataset(manifest, "train", config["context"], config["stride"],
                               2*mcfg.patch_size, allowed_domain_ids=pretrain_ids,
                               domain_registry=domain_registry)
    val_data = WindowDataset(manifest, "val", config["context"], config["context"],
                             2*mcfg.patch_size, allowed_domain_ids=pretrain_ids,
                             domain_registry=domain_registry)
    # num_workers=0 keeps platform behavior identical and avoids unnecessary RAM copies.
    valid_loader = DataLoader(val_data, batch_size=config["batch_size"], collate_fn=collate_windows)
    run = dict(config=config, device=str(device), torch_version=str(torch.__version__),
               parameters=sum(p.numel() for p in model.parameters()), manifest_sha256=digest,
               domain_registry_sha256=sha256(domain_registry) if domain_registry else None,
               train_windows=len(train_data), val_windows=len(val_data),
               skipped_train_windows=train_data.skipped_windows, skipped_val_windows=val_data.skipped_windows,
               train_domains=sorted({r["domain"] for r in train_data.records}),
               backbone_provenance=backbone_provenance(model), execution_provenance=execution)
    if mcfg.backbone == "fly_sparse":
        run["graph_provenance"] = graph_provenance(model)
    (outdir / "run.json").write_text(json.dumps(run, indent=2)+"\n")
    print(json.dumps(run), flush=True)
    step_seconds = []
    setup_seconds = time.perf_counter() - process_started
    training_step_seconds = 0.0
    validation_seconds = 0.0
    checkpoint_seconds = 0.0
    for epoch in range(start, config["epochs"]):
        tick = time.perf_counter()
        setup_started = tick
        # Epoch-indexed sampling/corruption enables exact CPU epoch-boundary resume.
        sample_rng = torch.Generator().manual_seed(seed+epoch)
        mask_rng = torch.Generator(device=device).manual_seed(seed+10000+epoch)
        channel_rng = torch.Generator(device=device).manual_seed(seed+30000+epoch)
        dropout_rng = torch.Generator(device=device).manual_seed(seed+40000+epoch)
        sampler = train_data.balanced_sampler(config["steps_per_epoch"]*config["batch_size"], sample_rng)
        loader = DataLoader(train_data, batch_size=config["batch_size"], sampler=sampler, collate_fn=collate_windows)
        setup_seconds += time.perf_counter() - setup_started
        training_started = time.perf_counter()
        model.train()
        losses = []
        iterator = iter(loader)
        for _ in range(config["steps_per_epoch"]):
            step_started = time.perf_counter()
            batch = next(iterator)
            batch = move(batch, device)
            optimizer.zero_grad(set_to_none=True)
            result = forward_batch(model, batch, masking, mask_rng, channel_rng, dropout_rng)
            loss = reconstruction_loss(result)
            if not torch.isfinite(loss):
                raise FloatingPointError("non-finite training loss")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
            optimizer.step()
            losses.append(loss.item())
            step_seconds.append(time.perf_counter() - step_started)
        training_step_seconds += time.perf_counter() - training_started
        validation_started = time.perf_counter()
        model.eval()
        val_rng = torch.Generator(device=device).manual_seed(seed+20000)
        val_channel_rng = torch.Generator(device=device).manual_seed(seed+50000)
        validation_rows = []
        baseline_rows = []
        selected_records = set()
        with torch.no_grad():
            for j, batch in enumerate(valid_loader):
                if config.get("val_batches", 0) and j >= config["val_batches"]:
                    break
                result = forward_batch(model, move(batch, device), masking, val_rng,
                                       val_channel_rng, validation=True)
                for i, (domain_id, record_id) in enumerate(zip(batch["domain_id"], batch["record_id"])):
                    selected_records.add((domain_id, record_id))
                    mask = result["target_mask"][i]
                    if mask.any():
                        count = int(mask.sum().item())
                        value = torch.nn.functional.smooth_l1_loss(
                            result["prediction"][i][mask], result["target"][i][mask], beta=1.0,
                            reduction="sum").item()
                        validation_rows.append((domain_id, record_id, value, count))
                        baseline = torch.nn.functional.smooth_l1_loss(
                            torch.zeros_like(result["target"][i][mask]), result["target"][i][mask], beta=1.0,
                            reduction="sum").item()
                        baseline_rows.append((domain_id, record_id, baseline, count))
        required_records = (selected_records if config.get("val_batches", 0) else
                            {(r.get("domain_id", r["dataset"]), rid)
                             for rid, r in zip(val_data.record_ids, val_data.records)})
        val, by_domain = validation_losses(validation_rows, required_records)
        baseline_val, _ = validation_losses(baseline_rows, required_records)
        if not math.isfinite(val):
            raise FloatingPointError("non-finite or empty validation")
        validation_seconds += time.perf_counter() - validation_started
        checkpoint_started = time.perf_counter()
        row = dict(epoch=epoch+1, train_loss=sum(losses)/len(losses), val_loss=val,
                   val_by_domain=by_domain, seconds=time.perf_counter()-tick,
                   val_visible_mean_baseline=baseline_val,
                   tau=(model.graph.tau.detach().cpu().tolist()
                        if mcfg.backbone == "fly_sparse" else None))
        history.append(row)
        improved = val < best
        best = min(best, val)
        save_checkpoint(outdir / "last.pt", model, optimizer, epoch+1, config, digest, history, best, execution)
        if improved:
            save_checkpoint(outdir / "best.pt", model, optimizer, epoch+1, config, digest, history, best, execution)
        (outdir / "history.json").write_text(json.dumps(history, indent=2)+"\n")
        print(json.dumps(row), flush=True)
        checkpoint_seconds += time.perf_counter() - checkpoint_started
    resource = dict(wall_seconds=time.perf_counter() - process_started,
                    setup_seconds=setup_seconds,
                    training_step_seconds=training_step_seconds,
                    validation_seconds=validation_seconds,
                    checkpoint_seconds=checkpoint_seconds,
                    steady_step_seconds=(sum(step_seconds[1:]) / len(step_seconds[1:])
                                         if len(step_seconds) > 1 else None),
                    measured_steps=len(step_seconds), peak_rss_bytes=peak_rss_bytes(),
                    threads=torch.get_num_threads(), dtype="float32", device=str(device))
    (outdir / "resource.json").write_text(json.dumps(resource, indent=2) + "\n", encoding="utf-8")
    return history


def embed(manifest, checkpoint, output, split="test", device="auto", context=256,
          domain_registry=None):
    """Export embeddings + dataset provenance for retrieval/clustering/probes."""
    verify_corpus(manifest, domain_registry)
    registry = load_domain_registry(manifest, domain_registry)
    if registry and split == "test":
        raise ValueError("canonical corpus development embedding forbids test split")
    model, _ = load_encoder(checkpoint, device)
    device = next(model.parameters()).device
    allowed = ({key for key, role in registry["roles"].items() if role != "final-held-out"}
               if registry else None)
    data = WindowDataset(manifest, split, context, context, 2*model.config.patch_size,
                         allowed_domain_ids=allowed, domain_registry=domain_registry)
    loader = DataLoader(data, batch_size=16, collate_fn=collate_windows)
    embeddings, labels, names = [], [], []
    with torch.no_grad():
        for batch in loader:
            args = move(batch, device)
            z = model.encode(args["x"], args["observed"], args["dt"], args["time_known"],
                             args["lengths"], args.get("channel_counts"))
            embeddings.append(z["global"].cpu().numpy())
            labels.extend(batch["label"].tolist())
            names.extend(batch["dataset"])
    with Path(output).open("xb") as stream:
        np.savez_compressed(stream, embeddings=np.concatenate(embeddings), labels=labels, datasets=names)
    return len(labels)


def probe(manifest, checkpoint, dataset, device="auto", context=128, domain_registry=None):
    """Frozen encoder + train-standardized ridge linear classifier, no fine-tuning.

    Alpha selected on validation only; official test used once. Labels never
    participate in pretraining. This is a sanity check, not proof of cross-domain transfer.
    """
    verify_corpus(manifest, domain_registry)
    registry = load_domain_registry(manifest, domain_registry)
    if registry:
        raise ValueError("canonical corpus probe requires separately approved final-held-out access")
    model, _ = load_encoder(checkpoint, device)
    device = next(model.parameters()).device
    sets = {}
    with torch.no_grad():
        for split in ("train", "val", "test"):
            data = WindowDataset(manifest, split, context, context, 2*model.config.patch_size)
            selected = [i for i, (r, _, _) in enumerate(data.windows)
                        if data.records[r]["dataset"] == dataset and "label" in data.records[r]]
            if not selected:
                raise ValueError(f"no labeled {split} examples for {dataset}")
            rows, labels = [], []
            for batch in DataLoader(torch.utils.data.Subset(data, selected), batch_size=32, collate_fn=collate_windows):
                args = move(batch, device)
                rows.append(model.encode(args["x"], args["observed"], args["dt"],
                                         args["time_known"], args["lengths"],
                                         args.get("channel_counts"))["global"].cpu())
                labels.append(batch["label"])
            sets[split] = (torch.cat(rows).double(), torch.cat(labels))
    x, y = sets["train"]
    mean, scale = x.mean(0), x.std(0).clamp_min(1e-5)
    classes = y.unique(sorted=True)
    if len(classes) < 2:
        raise ValueError("probe needs at least two train classes")
    features = {key: torch.cat([(a-mean)/scale, torch.ones(len(a), 1)], 1) for key, (a, _) in sets.items()}
    target = (y[:, None] == classes).double()
    best = None
    for alpha in (0.01, 0.1, 1., 10., 100.):
        x = features["train"]
        penalty = torch.eye(x.shape[1], dtype=x.dtype)*alpha
        penalty[-1, -1] = 0
        weight = torch.linalg.solve(x.T@x + penalty, x.T@target)
        prediction = classes[(features["val"]@weight).argmax(1)]
        score = (prediction == sets["val"][1]).double().mean().item()
        if best is None or score > best[0]:
            best = (score, alpha, weight)
    predicted = classes[(features["test"]@best[2]).argmax(1)]
    test_y = sets["test"][1]
    recalls = [(predicted[test_y == c] == c).double().mean().item() for c in test_y.unique()]
    return dict(dataset=dataset, val_accuracy=best[0], alpha=best[1],
                test_accuracy=(predicted == test_y).double().mean().item(),
                test_balanced_accuracy=sum(recalls)/len(recalls),
                counts={key: len(value[1]) for key, value in sets.items()})
