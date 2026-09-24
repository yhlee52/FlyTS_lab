"""CPU/CUDA trainer, local checkpoints and frozen-encoder evaluation. No network."""
from dataclasses import asdict
import json
import math
from pathlib import Path
import random
import time

import numpy as np
import torch
from torch.utils.data import DataLoader

from .corpus import WindowDataset, collate_windows, sha256, verify_corpus
from .foundation import EncoderConfig, FlyTSFoundation, reconstruction_loss, sample_hide


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


def forward_batch(model, batch, ratio, generator):
    hidden = sample_hide(batch["observed"], model.config.patch_size, ratio, generator)
    return model(batch["x"], batch["observed"], batch["dt"], hide=hidden,
                 time_known=batch["time_known"], lengths=batch["lengths"])


def save_checkpoint(path, model, optimizer, epoch, config, manifest_hash, history, best):
    state = dict(format_version=1, model_config=asdict(model.config), model=model.state_dict(),
                 optimizer=optimizer.state_dict(), epoch=epoch, training_config=config,
                 manifest_sha256=manifest_hash, history=history, best=best,
                 torch_rng=torch.get_rng_state(),
                 cuda_rng=torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [])
    temp = Path(str(path)+".tmp")
    torch.save(state, temp)
    temp.replace(path)


def load_encoder(checkpoint, device="cpu"):
    device = resolve_device(device)
    # Tensor/basic-type checkpoint only. Never deserialize arbitrary pickled models.
    state = torch.load(checkpoint, map_location="cpu", weights_only=True)
    if state.get("format_version") != 1:
        raise ValueError("unknown checkpoint version")
    model = FlyTSFoundation(EncoderConfig(**state["model_config"]))
    model.load_state_dict(state["model"])
    return model.to(device).eval(), state


def train(manifest, config_path, output, device="auto", resume=None, epochs=None):
    config = json.loads(Path(config_path).read_text())
    if epochs is not None:
        config["epochs"] = epochs
    for key in ("epochs", "batch_size", "steps_per_epoch", "context", "stride", "threads"):
        if config[key] < 1:
            raise ValueError(f"{key} must be positive")
    if not 0 < config["mask_ratio"] < 1 or config["lr"] <= 0:
        raise ValueError("invalid mask ratio/learning rate")
    device = resolve_device(device)
    torch.set_num_threads(config["threads"])
    seed = config["seed"]
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    verify_corpus(manifest)
    digest = sha256(manifest)
    mcfg = EncoderConfig(**config["model"])
    model = FlyTSFoundation(mcfg).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config["lr"], weight_decay=1e-4)
    start, history, best = 0, [], float("inf")
    if resume:
        restored, state = load_encoder(resume, device=str(device))
        if state["manifest_sha256"] != digest or state["model_config"] != asdict(mcfg):
            raise ValueError("resume requires identical model and corpus manifest")
        old = {k: v for k, v in state["training_config"].items() if k != "epochs"}
        new = {k: v for k, v in config.items() if k != "epochs"}
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
    train_data = WindowDataset(manifest, "train", config["context"], config["stride"], 2*mcfg.patch_size)
    val_data = WindowDataset(manifest, "val", config["context"], config["context"], 2*mcfg.patch_size)
    # num_workers=0 keeps platform behavior identical and avoids unnecessary RAM copies.
    valid_loader = DataLoader(val_data, batch_size=config["batch_size"], collate_fn=collate_windows)
    run = dict(config=config, device=str(device), torch_version=str(torch.__version__),
               parameters=sum(p.numel() for p in model.parameters()), manifest_sha256=digest,
               train_windows=len(train_data), val_windows=len(val_data),
               skipped_train_windows=train_data.skipped_windows, skipped_val_windows=val_data.skipped_windows,
               train_domains=sorted({r["domain"] for r in train_data.records}))
    (outdir / "run.json").write_text(json.dumps(run, indent=2)+"\n")
    print(json.dumps(run), flush=True)
    for epoch in range(start, config["epochs"]):
        tick = time.perf_counter()
        # Epoch-indexed sampling/corruption enables exact CPU epoch-boundary resume.
        sample_rng = torch.Generator().manual_seed(seed+epoch)
        mask_rng = torch.Generator(device=device).manual_seed(seed+10000+epoch)
        sampler = train_data.balanced_sampler(config["steps_per_epoch"]*config["batch_size"], sample_rng)
        loader = DataLoader(train_data, batch_size=config["batch_size"], sampler=sampler, collate_fn=collate_windows)
        model.train()
        losses = []
        for batch in loader:
            batch = move(batch, device)
            optimizer.zero_grad(set_to_none=True)
            result = forward_batch(model, batch, config["mask_ratio"], mask_rng)
            loss = reconstruction_loss(result)
            if not torch.isfinite(loss):
                raise FloatingPointError("non-finite training loss")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
            optimizer.step()
            losses.append(loss.item())
        model.eval()
        val_rng = torch.Generator(device=device).manual_seed(seed+20000)
        domain_losses = {}
        domain_baselines = {}
        with torch.no_grad():
            for j, batch in enumerate(valid_loader):
                if config.get("val_batches", 0) and j >= config["val_batches"]:
                    break
                result = forward_batch(model, move(batch, device), config["mask_ratio"], val_rng)
                for i, domain in enumerate(batch["domain"]):
                    mask = result["target_mask"][i]
                    if mask.any():
                        value = torch.nn.functional.smooth_l1_loss(
                            result["prediction"][i][mask], result["target"][i][mask]).item()
                        domain_losses.setdefault(domain, []).append(value)
                        baseline = torch.nn.functional.smooth_l1_loss(
                            torch.zeros_like(result["target"][i][mask]), result["target"][i][mask]).item()
                        domain_baselines.setdefault(domain, []).append(baseline)
        by_domain = {key: sum(vals)/len(vals) for key, vals in domain_losses.items()}
        val = sum(by_domain.values())/len(by_domain) if by_domain else float("nan")
        if not math.isfinite(val):
            raise FloatingPointError("non-finite or empty validation")
        row = dict(epoch=epoch+1, train_loss=sum(losses)/len(losses), val_loss=val,
                   val_by_domain=by_domain, seconds=time.perf_counter()-tick,
                   val_visible_mean_baseline=sum(sum(v)/len(v) for v in domain_baselines.values())/len(domain_baselines),
                   tau=model.graph.tau.detach().cpu().tolist())
        history.append(row)
        improved = val < best
        best = min(best, val)
        save_checkpoint(outdir / "last.pt", model, optimizer, epoch+1, config, digest, history, best)
        if improved:
            save_checkpoint(outdir / "best.pt", model, optimizer, epoch+1, config, digest, history, best)
        (outdir / "history.json").write_text(json.dumps(history, indent=2)+"\n")
        print(json.dumps(row), flush=True)
    return history


def embed(manifest, checkpoint, output, split="test", device="auto", context=256):
    """Export embeddings + dataset provenance for retrieval/clustering/probes."""
    verify_corpus(manifest)
    model, _ = load_encoder(checkpoint, device)
    device = next(model.parameters()).device
    data = WindowDataset(manifest, split, context, context, 2*model.config.patch_size)
    loader = DataLoader(data, batch_size=16, collate_fn=collate_windows)
    embeddings, labels, names = [], [], []
    with torch.no_grad():
        for batch in loader:
            args = move(batch, device)
            z = model.encode(args["x"], args["observed"], args["dt"], args["time_known"], args["lengths"])
            embeddings.append(z["global"].cpu().numpy())
            labels.extend(batch["label"].tolist())
            names.extend(batch["dataset"])
    with Path(output).open("xb") as stream:
        np.savez_compressed(stream, embeddings=np.concatenate(embeddings), labels=labels, datasets=names)
    return len(labels)


def probe(manifest, checkpoint, dataset, device="auto", context=128):
    """Frozen encoder + train-standardized ridge linear classifier, no fine-tuning.

    Alpha selected on validation only; official test used once. Labels never
    participate in pretraining. This is a sanity check, not proof of cross-domain transfer.
    """
    verify_corpus(manifest)
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
                rows.append(model.encode(args["x"], args["observed"], args["dt"], args["time_known"], args["lengths"])["global"].cpu())
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
