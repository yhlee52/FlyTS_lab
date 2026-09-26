"""Small, offline-first multivariate representation learner (not a pretrained FM).

The graph is synthetic fly-inspired, NOT a measured fly connectome. Channel
ordering is equivariant; channel identities/units are not inferred from indices.
"""
from dataclasses import dataclass
import math

import torch
from torch import nn
from torch.nn import functional as F

from .masking import MaskPlan
from .topology import build_topology


@dataclass(frozen=True)
class EncoderConfig:
    patch_size: int = 8
    width: int = 64
    hidden: int = 128
    slots: int = 4
    populations: int = 16
    density: float = 0.1
    tau_min: float = 0.05
    tau_max: float = 3_000_000.0
    topology_seed: int = 7
    backend: str = "dense"
    topology: str = "fly_like"
    topology_control_seed: int | None = None

    def __post_init__(self):
        if min(self.patch_size, self.width, self.hidden, self.slots) < 1:
            raise ValueError("model sizes must be positive")
        if not 1 <= self.populations <= self.hidden or self.hidden < 2:
            raise ValueError("invalid populations/hidden")
        if not 0 < self.density <= 1:
            raise ValueError("density must be in (0, 1]")
        if not 0 < self.tau_min < self.tau_max < float("inf"):
            raise ValueError("invalid tau bounds")
        if self.backend not in ("dense", "scatter"):
            raise ValueError("backend must be dense or scatter")
        if self.topology not in ("fly_like", "degree_preserving_rewired", "random_sparse"):
            raise ValueError(f"unknown topology kind {self.topology!r}")
        if self.topology != "fly_like" and (isinstance(self.topology_control_seed, bool)
                or not isinstance(self.topology_control_seed, int)):
            raise ValueError("control topology requires explicit integer topology_control_seed")


class PopulationGraph(nn.Module):
    """Type-pair tied edge weights; equivalent dense/scatter implementations.

    Dense is often faster for small graphs. Scatter does not guarantee a speedup.
    State integration is a leaky discrete update, not an exact nonlinear ODE solve.
    """
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        pop = torch.arange(cfg.hidden) * cfg.populations // cfg.hidden
        graph = build_topology(cfg.topology, hidden_size=cfg.hidden,
                               num_modules=min(4, cfg.hidden),
                               num_populations=cfg.populations, population=pop,
                               sparsity=1-cfg.density, seed=cfg.topology_seed,
                               control_seed=cfg.topology_control_seed)
        self.artifact = graph
        self.register_buffer("dst", graph.dst)
        self.register_buffer("src", graph.src)
        self.register_buffer("pop", graph.population)
        self.register_buffer("edge_type", graph.edge_type)
        # L1-normalized incoming weights keep recurrence non-expansive in infinity norm.
        self.register_buffer("degree", graph.degree)
        self.type_weight = nn.Parameter(torch.randn(cfg.populations**2) * 0.2)
        self.tau_logits = nn.Parameter(torch.linspace(-3, 3, cfg.populations))
        self.drive = nn.Linear(cfg.slots * cfg.width, cfg.hidden)
        self.bias = nn.Parameter(torch.zeros(cfg.hidden))
        self.out = nn.Linear(cfg.hidden, cfg.width)

    @property
    def tau(self):
        c = self.cfg
        return c.tau_min * torch.exp(self.tau_logits.sigmoid() * math.log(c.tau_max/c.tau_min))

    def forward(self, slots, delta, valid):
        b, p, _, _ = slots.shape
        drives = self.drive(slots.flatten(-2))
        weights = self.type_weight.tanh()[self.edge_type] / self.degree[self.dst]
        dense = None
        if self.cfg.backend == "dense":
            dense = weights.new_zeros(self.cfg.hidden, self.cfg.hidden)
            dense = dense.index_put((self.dst, self.src), weights)
        state = drives.new_zeros(b, self.cfg.hidden)
        states = []
        tau = self.tau[self.pop]
        for t in range(p):
            if dense is None:
                rec = state.new_zeros(state.shape).index_add(
                    1, self.dst, state[:, self.src] * weights)
            else:
                rec = F.linear(state, dense)
            alpha = -torch.expm1(-delta[:, t, None] / tau)
            update = state + alpha * (torch.tanh(drives[:, t] + rec + self.bias) - state)
            state = torch.where(valid[:, t, None], update, state)
            states.append(state)
        return self.out(torch.stack(states, dim=1))


class FlyTSFoundation(nn.Module):
    """Shared-weight encoder for arbitrary positive T and C, input [B,T,C].

    observed distinguishes missing/padding from zero. hide is a separate
    self-supervised corruption mask [B,P,C]. Normalization sees ONLY visible
    values: held-out targets cannot leak into input statistics.
    """
    def __init__(self, config=EncoderConfig()):
        super().__init__()
        self.config = config
        d, k = config.width, config.patch_size
        self.tokenizer = nn.Sequential(nn.Linear(2*k, d), nn.GELU(), nn.Linear(d, d))
        self.stats = nn.Linear(2, d)
        self.clock = nn.Linear(4, d)
        self.queries = nn.Parameter(torch.randn(config.slots, d) / math.sqrt(d))
        self.key = nn.Linear(d, d, bias=False)
        self.value = nn.Linear(d, d, bias=False)
        self.graph = PopulationGraph(config)
        self.context = nn.Sequential(nn.Linear(3*d, d), nn.GELU(), nn.LayerNorm(d))
        self.decoder = nn.Linear(d, k)

    def forward(self, x, observed=None, dt=1.0, hide=None, time_known=None, lengths=None,
                mask_plan=None, channel_counts=None):
        if x.ndim != 3 or min(x.shape) < 1 or not x.is_floating_point():
            raise ValueError("x must be a nonempty floating [B,T,C] tensor")
        b, t, c = x.shape
        lengths = torch.full((b,), t, device=x.device) if lengths is None else lengths.to(x.device)
        if lengths.shape != (b,) or (lengths < 1).any() or (lengths > t).any():
            raise ValueError("lengths must be [B] within [1,T]")
        if observed is not None and observed.shape != x.shape:
            raise ValueError("observed must match x")
        channel_counts = (torch.full((b,), c, device=x.device) if channel_counts is None
                          else torch.as_tensor(channel_counts, device=x.device))
        if channel_counts.shape != (b,) or channel_counts.dtype not in (torch.int8, torch.int16,
                torch.int32, torch.int64, torch.uint8) or (channel_counts < 1).any() or (channel_counts > c).any():
            raise ValueError("channel_counts must be integer [B] within [1,C]")
        present = torch.arange(t, device=x.device)[None] < lengths[:, None]
        channel_present = torch.arange(c, device=x.device)[None] < channel_counts[:, None]
        sample_padding = ~(present[..., None] & channel_present[:, None, :])
        observed = ((torch.isfinite(x) if observed is None else observed.bool() & torch.isfinite(x))
                    & ~sample_padding)
        missing = ~observed & ~sample_padding
        if not observed.flatten(1).any(1).all():
            raise ValueError("each record needs at least one observed value")
        x = torch.where(observed, x, torch.zeros_like(x))
        dt = torch.as_tensor(dt, dtype=x.dtype, device=x.device)
        if dt.ndim == 0:
            dt = dt.expand(b)
        if dt.shape != (b,) or not torch.isfinite(dt).all() or (dt <= 0).any():
            raise ValueError("dt must be finite positive scalar or [B]")
        known = torch.ones_like(dt) if time_known is None else torch.as_tensor(
            time_known, device=x.device, dtype=x.dtype).expand(b)
        k = self.config.patch_size
        p = (t+k-1)//k
        # B,P,C,K, preserving intra-patch samples rather than averaging spikes away.
        patches = F.pad(x.transpose(1, 2), (0, p*k-t)).unfold(-1, k, k).transpose(1, 2)
        obs = F.pad(observed.transpose(1, 2), (0, p*k-t)).unfold(-1, k, k).transpose(1, 2)
        missing_patches = F.pad(missing.transpose(1, 2), (0, p*k-t)).unfold(-1, k, k).transpose(1, 2)
        padding_patches = ~F.pad((~sample_padding).transpose(1, 2), (0, p*k-t)).unfold(-1, k, k).transpose(1, 2)
        if hide is not None and mask_plan is not None:
            raise ValueError("provide hide or mask_plan, not both")
        if mask_plan is not None:
            if not isinstance(mask_plan, MaskPlan):
                raise ValueError("mask_plan must be a MaskPlan")
            for cause in (mask_plan.temporal, mask_plan.channel, mask_plan.dropout):
                if cause.shape != (b, p, c) or cause.dtype != torch.bool or cause.device != x.device:
                    raise ValueError("mask_plan causes must be boolean [B,P,C] on x device")
            if (mask_plan.channel != mask_plan.channel[:, :1]).any() or (mask_plan.dropout != mask_plan.dropout[:, :1]).any():
                raise ValueError("channel and dropout causes must each cover full channels")
            if (mask_plan.channel & mask_plan.dropout).any():
                raise ValueError("channel and dropout causes cannot overlap")
            if not (obs & ~mask_plan.hide[..., None]).flatten(1).any(1).all():
                raise ValueError("mask_plan must retain an originally observed visible sample per record")
            hide = mask_plan.hide
        if hide is None:
            hide = torch.zeros((b, p, c), device=x.device, dtype=torch.bool)
        if hide.shape != (b, p, c) or hide.dtype != torch.bool:
            raise ValueError("hide must be boolean [B,ceil(T/patch_size),C]")
        visible = obs & ~hide[..., None]
        raw_count = visible.sum((1, 3))
        count = raw_count.clamp_min(1)
        channel_mean = (patches * visible).sum((1, 3)) / count
        pooled_count = visible.sum((1, 2, 3)).clamp_min(1)
        pooled_mean = (patches * visible).sum((1, 2, 3)) / pooled_count
        mean = torch.where(raw_count > 0, channel_mean, pooled_mean[:, None])
        centered = patches - mean[:, None, :, None]
        channel_variance = (centered.square() * visible).sum((1, 3)) / count
        pooled_variance = ((patches - pooled_mean[:, None, None, None]).square() * visible).sum((1, 2, 3)) / pooled_count
        variance = torch.where(raw_count > 0, channel_variance, pooled_variance[:, None])
        scale = variance.sqrt().clamp_min(0.01)
        normalized = centered / scale[:, None, :, None]
        tokens = self.tokenizer(torch.cat([
            torch.where(visible, normalized, torch.zeros_like(normalized)), visible.to(x.dtype)
        ], -1))
        stat = torch.stack([mean.sign()*torch.log1p(mean.abs()), scale.log()], -1)
        tokens = tokens + self.stats(stat)[:, None]
        index = torch.arange(p, device=x.device, dtype=x.dtype)
        clock = torch.stack([
            dt.log()[:, None].expand(b, p), known[:, None].expand(b, p),
            torch.sin(index/10)[None].expand(b, p), torch.cos(index/10)[None].expand(b, p)
        ], -1)
        tokens = tokens + self.clock(clock)[:, :, None]
        available = visible.any(-1)
        # Per-channel identity comes from visible content, not dataset-specific channel IDs.
        channel_context = (tokens * available[..., None]).sum(1) / available.sum(1).clamp_min(1)[..., None]
        scores = torch.einsum("md,bpcd->bpmc", self.queries, self.key(tokens)) / math.sqrt(self.config.width)
        weights = scores.masked_fill(~available[:, :, None], -1e4).softmax(-1)
        weights = weights * available[:, :, None]
        weights = weights / weights.sum(-1, keepdim=True).clamp_min(1e-8)
        slots = torch.einsum("bpmc,bpcd->bpmd", weights, self.value(tokens))
        # Real patch duration, including partial final patch; fully padded steps freeze state.
        time_present = F.pad(present, (0, p*k-t)).reshape(b, p, k).sum(-1)
        patch_valid = time_present > 0
        delta = time_present.to(x.dtype) * dt[:, None]
        temporal = self.graph(slots, delta, patch_valid)
        contextual = self.context(torch.cat([
            tokens, temporal[:, :, None].expand(-1, -1, c, -1),
            channel_context[:, None].expand(-1, p, -1, -1)
        ], -1))
        valid = obs.any(-1)
        contextual = contextual * valid[..., None]
        channel = contextual.sum(1) / valid.sum(1).clamp_min(1)[..., None]
        global_embedding = (temporal * patch_valid[..., None]).sum(1) / patch_valid.sum(1).clamp_min(1)[:, None]
        pred = self.decoder(contextual)
        reconstruction = (pred * scale[:, None, :, None] + mean[:, None, :, None])
        reconstruction = reconstruction.transpose(1, 2).flatten(2).transpose(1, 2)[:, :t]
        temporal_target = obs & (mask_plan.temporal[..., None] if mask_plan is not None else hide[..., None])
        channel_target = (obs & mask_plan.channel[..., None] if mask_plan is not None else torch.zeros_like(obs))
        dropout_samples = (obs & mask_plan.dropout[..., None] if mask_plan is not None else torch.zeros_like(obs))
        temporal_target = temporal_target & ~channel_target & ~dropout_samples
        channel_target = channel_target & ~dropout_samples
        return {"global": global_embedding, "channel": channel,
                "time": temporal * patch_valid[..., None], "patch_channel": contextual,
                "prediction": pred, "target": normalized,
                "target_mask": temporal_target | channel_target,
                "temporal_target_mask": temporal_target, "channel_target_mask": channel_target,
                "dropout_mask": dropout_samples, "visible_mask": visible,
                "observed_mask": obs, "missing_mask": missing_patches,
                "padding_mask": padding_patches, "hidden_patch_mask": hide,
                "reconstruction": reconstruction, "patch_valid": patch_valid}

    def encode(self, x, observed=None, dt=1.0, time_known=None, lengths=None,
               channel_counts=None):
        """Use eval() and torch.no_grad() for frozen inference; returns unnormalized embeddings."""
        out = self(x, observed, dt, time_known=time_known, lengths=lengths,
                   channel_counts=channel_counts)
        return {key: out[key] for key in ("global", "time", "channel", "patch_channel")}


def sample_hide(observed, patch_size, ratio=0.4, generator=None):
    """Mask complete time patches across channels, leaving visible context per record."""
    if not 0 < ratio < 1:
        raise ValueError("mask ratio must be in (0, 1)")
    b, t, c = observed.shape
    p = (t+patch_size-1)//patch_size
    valid = F.pad(observed.transpose(1, 2), (0, p*patch_size-t)).unfold(-1, patch_size, patch_size).any(-1).any(1)
    hidden = torch.zeros((b, p), device=observed.device, dtype=torch.bool)
    for i in range(b):
        candidates = valid[i].nonzero().flatten()
        if len(candidates) < 2:
            raise ValueError("each window needs at least two observed patches")
        order = torch.randperm(len(candidates), generator=generator, device=observed.device)
        n = min(len(candidates)-1, max(1, round(len(candidates)*ratio)))
        hidden[i, candidates[order[:n]]] = True
    return hidden[..., None].expand(-1, -1, c)


def reconstruction_loss(out):
    mask = out["target_mask"]
    if not mask.any():
        raise ValueError("no observed masked targets")
    # Huber prevents one unusually large physical signal from dominating the batch.
    return F.smooth_l1_loss(out["prediction"][mask], out["target"][mask], beta=1.0)
