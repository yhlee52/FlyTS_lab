"""Independent corruption causes for patch reconstruction."""
from dataclasses import dataclass
import math

import torch
from torch.nn import functional as F


@dataclass(frozen=True)
class MaskingConfig:
    temporal_ratio: float = 0.4
    channel_ratio: float = 0.0
    channel_dropout_ratio: float = 0.0

    def __post_init__(self):
        values = (self.temporal_ratio, self.channel_ratio, self.channel_dropout_ratio)
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or
               not math.isfinite(v) or not 0 <= v < 1 for v in values):
            raise ValueError("masking ratios must be finite numbers in [0, 1)")
        if self.temporal_ratio + self.channel_ratio <= 0:
            raise ValueError("temporal and channel masking cannot both be zero")
        if self.channel_ratio + self.channel_dropout_ratio >= 1:
            raise ValueError("channel masking plus dropout must be below one")


def canonical_masking(config):
    """Validate either config spelling without modifying its stored form."""
    legacy, nested = "mask_ratio" in config, "masking" in config
    if legacy == nested:
        raise ValueError("provide exactly one of mask_ratio or masking")
    if legacy:
        return MaskingConfig(temporal_ratio=config["mask_ratio"])
    fields = config["masking"]
    if not isinstance(fields, dict) or set(fields) != {
            "temporal_ratio", "channel_ratio", "channel_dropout_ratio"}:
        raise ValueError("masking needs exactly three ratio fields")
    return MaskingConfig(**fields)


@dataclass(frozen=True)
class MaskPlan:
    temporal: torch.Tensor
    channel: torch.Tensor
    dropout: torch.Tensor

    @property
    def hide(self):
        return self.temporal | self.channel | self.dropout


def _rounded_count(count, ratio, generator, device):
    desired = count * ratio
    return math.floor(desired) + int(torch.rand((), generator=generator, device=device) < desired % 1)


def sample_mask_plan(observed, patch_size, masking, temporal_generator=None,
                     channel_generator=None, dropout_generator=None, lengths=None):
    """Sample dropout first, then target causes; reserve visible observed context."""
    # Import here to keep the pre-existing temporal algorithm and RNG calls exact.
    from .foundation import sample_hide
    if observed.ndim != 3 or observed.dtype != torch.bool or patch_size < 1:
        raise ValueError("observed must be boolean [B,T,C] and patch_size positive")
    b, t, c = observed.shape
    if lengths is not None:
        observed = observed & (torch.arange(t, device=observed.device)[None, :, None] < lengths[:, None, None])
    p = (t + patch_size - 1) // patch_size
    patch_obs = F.pad(observed.transpose(1, 2), (0, p*patch_size-t)).unfold(-1, patch_size, patch_size).any(-1).transpose(1, 2)
    dropout = torch.zeros((b, p, c), dtype=torch.bool, device=observed.device)
    channel = torch.zeros_like(dropout)
    for i in range(b):
        eligible = patch_obs[i].any(0).nonzero().flatten()
        if c > 1 and len(eligible) > 1 and masking.channel_dropout_ratio:
            n = min(len(eligible)-1, _rounded_count(len(eligible), masking.channel_dropout_ratio,
                                                    dropout_generator, observed.device))
            order = torch.randperm(len(eligible), generator=dropout_generator, device=observed.device)
            dropout[i, :, eligible[order[:n]]] = True
    temporal = (sample_hide(observed, patch_size, masking.temporal_ratio, temporal_generator)
                if masking.temporal_ratio else torch.zeros_like(dropout))
    for i in range(b):
        # If temporal masking removed the only surviving channel's samples,
        # restore one dropped channel that remains visible in time.
        available = patch_obs[i] & ~temporal[i] & ~dropout[i]
        if not available.any():
            rescue = (patch_obs[i] & ~temporal[i]).any(0).nonzero().flatten()
            if len(rescue):
                dropout[i, :, rescue[0]] = False
        eligible = (patch_obs[i].any(0) & ~dropout[i, 0]).nonzero().flatten()
        if c <= 1 or len(eligible) < 2 or not masking.channel_ratio:
            continue
        n = min(len(eligible)-1, _rounded_count(len(eligible), masking.channel_ratio,
                                                channel_generator, observed.device))
        order = torch.randperm(len(eligible), generator=channel_generator, device=observed.device)
        selected = eligible[order[:n]]
        channel[i, :, selected] = True
        if not (patch_obs[i] & ~temporal[i] & ~dropout[i] & ~channel[i]).any():
            # A fully masked record cannot supply visible statistics or context.
            survivors = (patch_obs[i] & ~temporal[i] & ~dropout[i]).any(0).nonzero().flatten()
            channel[i, :, survivors[0]] = False
    return MaskPlan(temporal, channel, dropout)
