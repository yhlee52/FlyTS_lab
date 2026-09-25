"""Offline, deterministic Stage 3 robustness evaluation. No final-test access."""
from collections import defaultdict
from dataclasses import dataclass
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import time
from typing import Protocol

import torch
from torch.nn import functional as F

from .corpus import WindowDataset, sha256, reject_forbidden, verify_development_corpus
from .masking import MaskPlan
from .training import load_encoder, resolve_device


FIXTURE_VERSION = "stage03-fixture-v1"


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def fixture_seed(config, manifest_hash, record_id, window_start, metric, repeat=0):
    payload = [1, config["master_seed"], manifest_hash, record_id, window_start, metric, repeat]
    return int(digest(payload)[:16], 16)


def order(items, seed):
    return sorted(items, key=lambda item: (digest([seed, int(item)]), int(item)))


def rounded_count(count, ratio, seed):
    wanted = count * ratio
    fractional = wanted - math.floor(wanted)
    u = int(digest([seed, "round"])[:13], 16) / 16**13
    return min(count - 1, math.floor(wanted) + int(u < fractional))


def nearest_seen(unseen, seen):
    if not seen:
        raise ValueError("training manifest has no seen channel counts")
    return min(seen, key=lambda n: (abs(n - unseen), n))


def count_candidates(seen, maximum):
    """Boundary and midpoint unseen counts, with interp/extrap labels."""
    seen = sorted(set(seen))
    if not seen or maximum < 1:
        raise ValueError("invalid channel-count range")
    candidates = set()
    for low, high in zip(seen, seen[1:]):
        for n in (low + 1, (low + high) // 2, high - 1):
            if low < n < high and n <= maximum:
                candidates.add(n)
    for n in (1, seen[0] - 1, seen[-1] + 1, maximum):
        if 1 <= n <= maximum and n not in seen:
            candidates.add(n)
    return [(n, "interpolation" if seen[0] < n < seen[-1] else "extrapolation")
            for n in sorted(candidates)]


def validate_config(config):
    expected = {"schema_version", "status", "master_seed", "split", "context",
                "temporal_ratio", "permutation_repeats", "dropout_repeats", "dropout_rates",
                "missing_repeats", "missing_rates", "missing_patterns", "relative_floor", "norm_floor"}
    if set(config) != expected or config["schema_version"] != 1 or config["status"] != "candidate":
        raise ValueError("unsupported evaluator config schema/status")
    if config["split"] not in ("train", "val"):
        raise ValueError("Stage 3 evaluator forbids test/final-held-out split")
    if config["dropout_rates"] != [0.0, 0.1, 0.3, 0.5] or config["missing_rates"] != [0.1, 0.3, 0.5]:
        raise ValueError("Stage 3 fixture rates are fixed")
    if config["missing_patterns"] != ["mcar", "block"]:
        raise ValueError("Stage 3 missingness patterns are fixed")
    if not 0 < config["temporal_ratio"] < 1 or config["temporal_ratio"] != 0.4:
        raise ValueError("Stage 3 reconstruction ratio is fixed at 0.4")
    for key in ("master_seed", "context", "permutation_repeats", "dropout_repeats", "missing_repeats"):
        if type(config[key]) is not int or config[key] < 1:
            raise ValueError(f"invalid {key}")
    if config["master_seed"] != 3007 or config["permutation_repeats"] != 8 or config["dropout_repeats"] != 8 or config["missing_repeats"] != 4:
        raise ValueError("Stage 3 fixture counts/seed differ from approved contract")
    for key in ("relative_floor", "norm_floor"):
        if type(config[key]) not in (float, int) or not math.isfinite(config[key]) or config[key] <= 0:
            raise ValueError(f"invalid candidate {key}")
    return config


def git_commit():
    root = Path(__file__).resolve().parents[2]
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def smooth_l1_shared(reconstruction, raw_target, target_mask, reference_mean, reference_scale):
    """Compare paired views in the same baseline-visible reference coordinates."""
    if not target_mask.any():
        raise ValueError("empty shared reconstruction target")
    pred = (reconstruction - reference_mean[None]) / reference_scale[None]
    target = (raw_target - reference_mean[None]) / reference_scale[None]
    loss = F.smooth_l1_loss(pred[target_mask], target[target_mask], beta=1.0)
    if not torch.isfinite(loss):
        raise FloatingPointError("non-finite reconstruction result")
    return float(loss.detach())


def relative_change(value, baseline, floor):
    difference = value - baseline
    if not math.isfinite(value) or not math.isfinite(baseline):
        raise FloatingPointError("non-finite paired result")
    return {"absolute_change": difference, "relative": difference / abs(baseline)
            if abs(baseline) >= floor else None,
            "status": "defined" if abs(baseline) >= floor else "undefined_small_denominator"}


def representation_distance(base, variant, floor):
    a, b = base.flatten().float(), variant.flatten().float()
    if not torch.isfinite(a).all() or not torch.isfinite(b).all():
        raise FloatingPointError("non-finite embedding")
    an, bn = float(torch.linalg.vector_norm(a)), float(torch.linalg.vector_norm(b))
    if an < floor or bn < floor:
        return {"primary": None, "relative_l2": None, "status": "undefined_zero_norm"}
    if torch.equal(a, b):
        return {"primary": 0.0, "relative_l2": 0.0, "status": "defined"}
    cosine = float(torch.dot(a.double(), b.double()) / (an * bn))
    return {"primary": 1.0 - max(-1.0, min(1.0, cosine)),
            "relative_l2": float(torch.linalg.vector_norm(a - b)) / an, "status": "defined"}


class EvaluatorAdapter(Protocol):
    """Minimal shared evaluator boundary for later backbone implementations."""
    patch_size: int

    def encode(self, x, observed, dt, time_known, length, channel_count): ...
    def reconstruct(self, x, observed, dt, time_known, length, channel_count, plan): ...
    def provenance(self): ...


@dataclass(frozen=True)
class FlyTSAdapter:
    model: object
    checkpoint_hash: str

    @property
    def patch_size(self):
        return self.model.config.patch_size

    def encode(self, x, observed, dt, time_known, length, channel_count):
        device = next(self.model.parameters()).device
        return self.model.encode(x.to(device)[None], observed.to(device)[None], dt.to(device)[None],
                                 time_known.to(device)[None],
                                 torch.tensor([length], device=device),
                                 torch.tensor([channel_count], device=device))["global"][0].cpu()

    def reconstruct(self, x, observed, dt, time_known, length, channel_count, plan):
        device = next(self.model.parameters()).device
        moved = MaskPlan(plan.temporal.to(device), plan.channel.to(device), plan.dropout.to(device))
        out = self.model(x.to(device)[None], observed.to(device)[None], dt.to(device)[None],
                         mask_plan=moved, time_known=time_known.to(device)[None],
                         lengths=torch.tensor([length], device=device),
                         channel_counts=torch.tensor([channel_count], device=device))
        return {"reconstruction": out["reconstruction"].cpu()}

    def provenance(self):
        return {"adapter": "flyts-v1", "checkpoint_sha256": self.checkpoint_hash}


def temporal_fixture(observed, patch_size, ratio, seed):
    t, c = observed.shape
    p = (t + patch_size - 1) // patch_size
    valid = [i for i in range(p) if observed[i*patch_size:(i+1)*patch_size].any()]
    if len(valid) < 2:
        raise ValueError("empty target or insufficient visible patches")
    selected = order(valid, seed)[:min(len(valid)-1, max(1, round(len(valid)*ratio)))]
    mask = torch.zeros((1, p, c), device=observed.device, dtype=torch.bool)
    mask[:, selected, :] = True
    return mask


def make_plan(temporal, removed=()):
    dropout = torch.zeros_like(temporal)
    if removed:
        dropout[:, :, list(removed)] = True
    return MaskPlan(temporal, torch.zeros_like(temporal), dropout)


def target_samples(observed, temporal, patch_size):
    return observed & temporal[0].repeat_interleave(patch_size, dim=0)[:observed.shape[0]]


def reference_stats(x, observed, target):
    visible = observed & ~target
    if not visible.any():
        raise ValueError("empty visible reference context")
    pooled = x[visible].mean()
    pooled_scale = x[visible].std(unbiased=False).clamp_min(0.01)
    mean, scale = [], []
    for j in range(x.shape[1]):
        values = x[:, j][visible[:, j]]
        mean.append(values.mean() if len(values) else pooled)
        scale.append(values.std(unbiased=False).clamp_min(0.01) if len(values) else pooled_scale)
    return torch.stack(mean), torch.stack(scale)


def _loss(adapter, x, observed, dt, known, plan, target, mean, scale):
    out = adapter.reconstruct(x, observed, dt, known, x.shape[0], x.shape[1], plan)
    return smooth_l1_shared(out["reconstruction"][0], torch.nan_to_num(x), target, mean, scale)


def _row(metric, arm, domain, record_id, window_start, value, **extra):
    if value is not None and not math.isfinite(value):
        raise FloatingPointError("non-finite evaluator row")
    return dict(metric=metric, arm=arm, domain=domain, record_id=record_id,
                window_start=window_start, value=value, **extra)


@torch.no_grad()
def evaluate_window(adapter, sample, config, manifest_hash, seen_counts):
    x = sample["x"]
    device = x.device
    observed = torch.isfinite(x)
    dt = torch.tensor(sample["dt"], dtype=x.dtype, device=device)
    known = torch.tensor(sample["time_known"], dtype=x.dtype, device=device)
    rid, start, domain = sample["record_id"], sample["window_start"], sample["domain"]
    seed = lambda metric, repeat=0: fixture_seed(config, manifest_hash, rid, start, metric, repeat)
    fixture = lambda metric, *parts: digest([FIXTURE_VERSION, manifest_hash, rid, start, metric, *parts])
    temporal = temporal_fixture(observed, adapter.patch_size, config["temporal_ratio"], seed("temporal"))
    target = target_samples(observed, temporal, adapter.patch_size)
    target_positions = target.nonzero().tolist()
    mean, scale = reference_stats(torch.nan_to_num(x), observed, target)
    baseline = _loss(adapter, x, observed, dt, known, make_plan(temporal), target, mean, scale)
    rows = [_row("reconstruction", "baseline", domain, rid, start, baseline,
                 target_count=int(target.sum()),
                 fixture_id=fixture("reconstruction", target_positions))]
    base_z = adapter.encode(x, observed, dt, known, len(x), x.shape[1])
    ident = representation_distance(base_z, base_z, config["norm_floor"])
    channels = list(range(x.shape[1]))
    rows.append(_row("permutation", "identity", domain, rid, start, ident["primary"],
                     relative_l2=ident["relative_l2"], status=ident["status"],
                     fixture_id=fixture("permutation", "identity", channels)))
    if len(channels) > 1:
        permutations = []
        for repeat in range(config["permutation_repeats"] * 4):
            perm = order(channels, seed("permutation", repeat))
            if perm != channels and perm not in permutations:
                permutations.append(perm)
            if len(permutations) >= config["permutation_repeats"]:
                break
        for repeat, perm in enumerate(permutations):
            variant = adapter.encode(x[:, perm], observed[:, perm], dt, known, len(x), len(perm))
            dist = representation_distance(base_z, variant, config["norm_floor"])
            rows.append(_row("permutation", f"perm_{repeat}", domain, rid, start, dist["primary"],
                             relative_l2=dist["relative_l2"], status=dist["status"],
                             fixture_id=fixture("permutation", repeat, perm)))
    eligible = [j for j in channels if observed[:, j].any()]
    for repeat in range(config["dropout_repeats"]):
        ranked = order(eligible, seed("dropout", repeat))
        for rate in config["dropout_rates"]:
            n = rounded_count(len(ranked), rate, seed("dropout-round", repeat)) if len(ranked) > 1 else 0
            removed = ranked[:n]
            shared = target.clone()
            if removed:
                shared[:, removed] = False
            pair_visible = observed.clone()
            if removed:
                pair_visible[:, removed] = False
            pair_mean, pair_scale = reference_stats(torch.nan_to_num(x), pair_visible, shared)
            base_loss = _loss(adapter, x, observed, dt, known, make_plan(temporal),
                              shared, pair_mean, pair_scale)
            loss = base_loss if rate == 0 else _loss(adapter, x, observed, dt, known,
                                                      make_plan(temporal, removed), shared,
                                                      pair_mean, pair_scale)
            delta = relative_change(loss, base_loss, config["relative_floor"])
            rows.append(_row("dropout", f"{int(rate*100)}%", domain, rid, start, delta["relative"],
                             baseline=base_loss, corrupted=loss, removed=removed,
                             target_count=int(shared.sum()),
                             fixture_id=fixture("dropout", repeat, rate, removed, shared.nonzero().tolist()),
                             **delta))
    # A count view is eligible only if both nested views exist on this source record.
    ranked = order(channels, seed("count-order"))
    for count, kind in count_candidates(seen_counts, len(channels)):
        near = nearest_seen(count, seen_counts)
        if near > len(channels):
            continue
        common = ranked[:min(count, near)]
        if not target[:, common].any():
            continue
        shared_mean, shared_scale = reference_stats(torch.nan_to_num(x[:, common]),
                                                     observed[:, common], target[:, common])
        losses = {}
        for n in (near, count):
            subset = ranked[:n]
            sub_temporal = temporal[:, :, subset]
            local_common = [subset.index(j) for j in common]
            sub_target = target[:, subset].clone()
            keep = torch.zeros(n, device=device, dtype=torch.bool)
            keep[local_common] = True
            sub_target &= keep[None]
            # Per-view predictions are converted to the same channel-wise reference coordinates.
            out = adapter.reconstruct(x[:, subset], observed[:, subset], dt, known,
                                      len(x), n, make_plan(sub_temporal))
            pred = out["reconstruction"][0][:, local_common]
            losses[n] = smooth_l1_shared(pred, torch.nan_to_num(x[:, common]), target[:, common],
                                         shared_mean, shared_scale)
        delta = relative_change(losses[count], losses[near], config["relative_floor"])
        rows.append(_row("channel_count", f"{kind}:{count}->{near}", domain, rid, start,
                         delta["relative"], unseen=count, nearest_seen=near, kind=kind,
                         baseline=losses[near], corrupted=losses[count],
                         target_count=int(target[:, common].sum()),
                         fixture_id=fixture("channel_count", count, near, ranked[:count],
                                            ranked[:near], target[:, common].nonzero().tolist()), **delta))
    # Added padding may not change the original representation or shared loss.
    for kind in ("time", "channel", "both"):
        xt, ot = x, observed
        if kind in ("time", "both"):
            pad = torch.full((adapter.patch_size, xt.shape[1]), float("nan"), device=device)
            xt = torch.cat((xt, pad), dim=0)
            ot = torch.cat((ot, torch.zeros_like(pad, dtype=torch.bool)), dim=0)
        if kind in ("channel", "both"):
            pad = torch.full((xt.shape[0], 1), float("nan"), device=device)
            xt = torch.cat((xt, pad), dim=1)
            ot = torch.cat((ot, torch.zeros_like(pad, dtype=torch.bool)), dim=1)
        z = adapter.encode(xt, ot, dt, known, len(x), x.shape[1])
        dist = representation_distance(base_z, z, config["norm_floor"])
        padded_temporal = torch.zeros((1, (len(xt)+adapter.patch_size-1)//adapter.patch_size,
                                       xt.shape[1]), device=device, dtype=torch.bool)
        padded_temporal[:, :temporal.shape[1], :temporal.shape[2]] = temporal
        padded_out = adapter.reconstruct(xt, ot, dt, known, len(x), x.shape[1],
                                          make_plan(padded_temporal))
        padded_loss = smooth_l1_shared(padded_out["reconstruction"][0][:len(x), :x.shape[1]],
                                       torch.nan_to_num(x), target, mean, scale)
        rows.append(_row("padding", kind, domain, rid, start, dist["primary"],
                         relative_l2=dist["relative_l2"],
                         max_abs=float((base_z-z).abs().max()),
                         shared_loss_change=padded_loss-baseline, status=dist["status"],
                         fixture_id=fixture("padding", kind, len(xt), xt.shape[1], target_positions)))
    context = (observed & ~target).nonzero().tolist()
    for pattern in config["missing_patterns"]:
        for repeat in range(config["missing_repeats"]):
            ranked_context = order(list(range(len(context))), seed(f"missing-{pattern}", repeat))
            for rate in config["missing_rates"]:
                n = min(len(context)-1, max(0, rounded_count(len(context), rate, seed("missing-round", repeat))))
                if pattern == "mcar":
                    chosen = ranked_context[:n]
                else:
                    # Stable contiguous slice in time order, allowing a partial final block.
                    first = seed("missing-block", repeat) % max(1, len(context)-n+1)
                    chosen = list(range(first, first+n))
                altered = observed.clone()
                for idx in chosen:
                    t, c = context[idx]
                    altered[t, c] = False
                if not (altered & ~target).any():
                    raise ValueError("missing fixture removed all visible context")
                pair_mean, pair_scale = reference_stats(torch.nan_to_num(x), altered, target)
                pair_baseline = _loss(adapter, x, observed, dt, known, make_plan(temporal),
                                      target, pair_mean, pair_scale)
                loss = _loss(adapter, x, altered, dt, known, make_plan(temporal),
                             target, pair_mean, pair_scale)
                delta = relative_change(loss, pair_baseline, config["relative_floor"])
                rows.append(_row("missing", f"{pattern}:{int(rate*100)}%", domain, rid, start,
                                 delta["relative"], baseline=pair_baseline, corrupted=loss,
                                 removed_count=n, target_count=int(target.sum()),
                                 fixture_id=fixture("missing", pattern, repeat, rate,
                                                    [context[idx] for idx in chosen], target_positions), **delta))
    return rows


def aggregate(rows, floor=1e-8):
    """Valid positions -> manifest record -> equal records/domain -> equal domains.

    Position-wise window means carry ``target_count``; representation windows
    have no position denominator and remain equal-weight within a record.
    """
    position_metrics = {"reconstruction", "dropout", "channel_count", "missing"}

    def record_mean(windows, field, position_metric):
        usable = [row for row in windows if row[field] is not None]
        if not usable:
            return None
        if position_metric:
            counts = [row.get("target_count") for row in usable]
            if any(type(n) is not int or n < 1 for n in counts):
                raise ValueError("position-wise rows require positive target_count")
            return sum(row[field] * n for row, n in zip(usable, counts)) / sum(counts)
        return sum(row[field] for row in usable) / len(usable)

    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for row in rows:
        grouped[(row["metric"], row["arm"])][row["domain"]][row["record_id"]].append(row)
    result = []
    for (metric, arm), domains in sorted(grouped.items()):
        by_domain, all_records, domain_losses = {}, [], []
        position_metric = metric in position_metrics
        paired = all("baseline" in row and "corrupted" in row
                     for records in domains.values() for windows in records.values() for row in windows)
        for domain, records in sorted(domains.items()):
            if paired:
                losses = [(record_mean(windows, "baseline", position_metric),
                           record_mean(windows, "corrupted", position_metric))
                          for _, windows in sorted(records.items())]
                base = sum(a for a, _ in losses)/len(losses)
                corrupt = sum(b for _, b in losses)/len(losses)
                by_domain[domain] = relative_change(corrupt, base, floor)["relative"]
                domain_losses.append((base, corrupt))
                all_records.extend(losses)
            else:
                values = [value for _, windows in sorted(records.items())
                          if (value := record_mean(windows, "value", position_metric)) is not None]
                by_domain[domain] = sum(values)/len(values) if values else None
                all_records.extend(values)
        valid_domains = [v for v in by_domain.values() if v is not None]
        if paired:
            macro_base = sum(a for a, _ in domain_losses)/len(domain_losses)
            macro_corrupt = sum(b for _, b in domain_losses)/len(domain_losses)
            primary = relative_change(macro_corrupt, macro_base, floor)["relative"]
            micro_base = sum(a for a, _ in all_records)/len(all_records)
            micro_corrupt = sum(b for _, b in all_records)/len(all_records)
            micro = relative_change(micro_corrupt, micro_base, floor)["relative"]
        else:
            primary = sum(valid_domains)/len(valid_domains) if valid_domains else None
            micro = sum(all_records)/len(all_records) if all_records else None
        result.append(dict(metric=metric, arm=arm,
                           domain_macro=primary, domains=by_domain, micro=micro,
                           worst_domain=max(valid_domains) if valid_domains else None,
                           records=len(all_records),
                           status="defined" if primary is not None else "undefined_small_denominator"))
    return result


def write_reports(output, rows, stable, runtime):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    rows = sorted(rows, key=lambda r: (r["domain"], r["record_id"], r["window_start"], r["metric"], r["arm"]))
    with (output / "records.jsonl").open("x", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
    result = {"schema_version": 1, "status": "candidate", "stable": stable, "runtime": runtime}
    (output / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    with (output / "summary.csv").open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("metric", "arm", "domain_macro", "micro", "worst_domain", "records"))
        writer.writeheader()
        writer.writerows({key: row[key] for key in writer.fieldnames} for row in stable["results"])
    lines = ["# Stage 3 robustness candidate", "", "| Metric | Arm | Domain macro | Micro | Worst domain | Records |",
             "|---|---|---:|---:|---:|---:|"]
    for row in stable["results"]:
        fmt = lambda value: f"{value:.17g}" if value is not None else "undefined"
        lines.append(f"| {row['metric']} | {row['arm']} | {fmt(row['domain_macro'])} | {fmt(row['micro'])} | {fmt(row['worst_domain'])} | {row['records']} |")
    (output / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result


def evaluate_robustness(manifest, checkpoint, config_path, output, device="cpu", split=None,
                        threads=2):
    """Evaluate local development data; never fetch or read test/final domains."""
    started = time.perf_counter()
    if type(threads) is not int or threads < 1:
        raise ValueError("threads must be positive")
    torch.set_num_threads(threads)
    config = validate_config(json.loads(Path(config_path).read_text(encoding="utf-8")))
    split = config["split"] if split is None else split
    if split not in ("train", "val"):
        raise ValueError("Stage 3 evaluator forbids test/final-held-out split")
    doc = verify_development_corpus(manifest, split)
    model, state = load_encoder(checkpoint, str(resolve_device(device)))
    manifest_hash = sha256(manifest)
    if state["manifest_sha256"] != manifest_hash:
        raise ValueError("checkpoint/manifest hash mismatch")
    adapter = FlyTSAdapter(model, sha256(checkpoint))
    seen = sorted({row["shape"][1] for row in doc["records"] if row["split"] == "train"})
    data = WindowDataset(manifest, split, config["context"], config["context"], 2*adapter.patch_size)
    rows = []
    with torch.no_grad():
        for i in range(len(data)):
            rows.extend(evaluate_window(adapter, data[i], config, manifest_hash, seen))
    results = aggregate(rows, config["relative_floor"])
    fixture_spec = {"fixture_version": FIXTURE_VERSION, "schema_version": 1,
                    "config": config, "manifest_sha256": manifest_hash,
                    "sampled_fixture_ids": sorted(row["fixture_id"] for row in rows)}
    training_config = state.get("training_config", {})
    steps = training_config.get("steps_per_epoch")
    epoch = state.get("epoch")
    checkpoint_training = {"seed": training_config.get("seed", "unavailable"),
                           "steps_per_epoch": steps if steps is not None else "unavailable",
                           "epochs_completed": epoch if epoch is not None else "unavailable",
                           "optimizer_steps": epoch * steps if isinstance(epoch, int) and isinstance(steps, int) else "unavailable",
                           "parameter_count": sum(parameter.numel() for parameter in model.parameters())}
    stable = {"provenance": {"git_commit": git_commit(),
                              "evaluator_source_sha256": sha256(__file__),
                              "manifest_sha256": manifest_hash,
                              "config_sha256": sha256(config_path), "evaluator_config": config,
                              "fixture_version": FIXTURE_VERSION, "checkpoint_training": checkpoint_training,
                              "split": split, "domains": sorted({r["domain"] for r in rows}),
                              "excluded_splits": ["test"], "seen_channel_counts": seen,
                              **adapter.provenance()},
              "fixture_sha256": digest(fixture_spec),
              "aggregation": {"position_metrics": ["reconstruction", "dropout", "channel_count", "missing"],
                              "within_record": "target_count_weighted_position_mean",
                              "representation_within_record": "equal_window_mean",
                              "within_domain": "equal_record_mean",
                              "across_domains": "equal_domain_mean",
                              "paired_degradation": "relative_difference_of_aggregated_arm_losses"},
              "results": results}
    runtime = {"device": str(next(model.parameters()).device), "threads": threads,
               "torch": torch.__version__,
               "python": platform.python_version(), "seconds": time.perf_counter()-started}
    return write_reports(output, rows, stable, runtime)
