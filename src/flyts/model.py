"""Fly-inspired sparse recurrent model with learnable physical time constants."""

from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor, nn


@dataclass(frozen=True)
class FlyRNNConfig:
    """Configuration for :class:`FlyRNN`.

    ``tau_min`` and ``tau_max`` use the same physical unit as ``dt``. The
    recommended convention is seconds.
    """

    input_size: int
    hidden_size: int = 64
    output_size: int = 2
    num_populations: int = 8
    num_modules: int = 4
    sparsity: float = 0.90
    reciprocal_fraction: float = 0.20
    hub_fraction: float = 0.08
    tau_min: float = 0.5
    tau_max: float = 30.0
    topology_seed: int = 7

    def __post_init__(self) -> None:
        if self.input_size <= 0 or self.hidden_size <= 1 or self.output_size <= 0:
            raise ValueError("input_size/output_size must be positive and hidden_size > 1")
        if not 1 <= self.num_populations <= self.hidden_size:
            raise ValueError("num_populations must be in [1, hidden_size]")
        if not 1 <= self.num_modules <= self.hidden_size:
            raise ValueError("num_modules must be in [1, hidden_size]")
        if not 0.0 <= self.sparsity < 1.0:
            raise ValueError("sparsity must be in [0, 1)")
        if not 0.0 <= self.reciprocal_fraction <= 1.0:
            raise ValueError("reciprocal_fraction must be in [0, 1]")
        if not 0.0 <= self.hub_fraction <= 1.0:
            raise ValueError("hub_fraction must be in [0, 1]")
        if self.tau_min <= 0 or self.tau_max <= self.tau_min:
            raise ValueError("tau bounds must satisfy 0 < tau_min < tau_max")


def _make_fly_mask(config: FlyRNNConfig) -> Tensor:
    """Create a reproducible sparse modular mask with reciprocal and hub edges."""

    n = config.hidden_size
    generator = torch.Generator().manual_seed(config.topology_seed)
    module = torch.arange(n) * config.num_modules // n

    base_density = 1.0 - config.sparsity
    same_module = module[:, None] == module[None, :]
    probabilities = torch.full((n, n), base_density * 0.55)
    probabilities[same_module] = min(1.0, base_density * 2.25)
    mask = torch.rand((n, n), generator=generator) < probabilities

    reciprocal_candidates = mask & ~mask.T
    add_reverse = (
        torch.rand((n, n), generator=generator) < config.reciprocal_fraction
    ) & reciprocal_candidates
    mask |= add_reverse.T

    hub_count = max(1, round(n * config.hub_fraction)) if config.hub_fraction else 0
    if hub_count:
        hubs = torch.randperm(n, generator=generator)[:hub_count]
        hub_density = min(0.50, max(0.15, base_density * 3.0))
        mask[hubs, :] |= torch.rand((hub_count, n), generator=generator) < hub_density
        mask[:, hubs] |= torch.rand((n, hub_count), generator=generator) < hub_density

    mask.fill_diagonal_(False)
    # Every neuron needs at least one incoming edge.
    for target in torch.where(mask.sum(dim=1) == 0)[0].tolist():
        source = (target + 1) % n
        mask[target, source] = True
    return mask.float()


class FlyRNNCell(nn.Module):
    """Continuous-time-inspired recurrent cell with fixed sparse topology."""

    def __init__(self, config: FlyRNNConfig) -> None:
        super().__init__()
        self.config = config
        self.input = nn.Linear(config.input_size, config.hidden_size)
        self.recurrent_weight = nn.Parameter(
            torch.empty(config.hidden_size, config.hidden_size)
        )
        self.recurrent_bias = nn.Parameter(torch.zeros(config.hidden_size))
        self.register_buffer("recurrent_mask", _make_fly_mask(config))

        population_index = torch.arange(config.hidden_size) % config.num_populations
        self.register_buffer("population_index", population_index)

        initial_fraction = torch.linspace(
            0.02, 0.98, config.num_populations, dtype=torch.float32
        )
        initial_logits = torch.logit(initial_fraction)
        self.tau_logits = nn.Parameter(initial_logits)
        self.reset_parameters()

    def reset_parameters(self) -> None:
        nn.init.xavier_uniform_(self.input.weight)
        nn.init.zeros_(self.input.bias)
        with torch.no_grad():
            fan_in = self.recurrent_mask.sum(dim=1).clamp_min(1.0).sqrt()
            self.recurrent_weight.normal_()
            self.recurrent_weight.div_(fan_in[:, None])
            self.recurrent_weight.mul_(self.recurrent_mask)

    @property
    def population_tau(self) -> Tensor:
        """Learnable population time constants, bounded in log space."""

        cfg = self.config
        log_ratio = math.log(cfg.tau_max / cfg.tau_min)
        return cfg.tau_min * torch.exp(torch.sigmoid(self.tau_logits) * log_ratio)

    @property
    def neuron_tau(self) -> Tensor:
        return self.population_tau[self.population_index]

    def forward(self, x_t: Tensor, state: Tensor, dt: float | Tensor) -> Tensor:
        if isinstance(dt, Tensor):
            if torch.any(dt <= 0):
                raise ValueError("dt must be positive")
            dt_tensor = dt.to(device=x_t.device, dtype=x_t.dtype)
        else:
            if dt <= 0:
                raise ValueError("dt must be positive")
            dt_tensor = x_t.new_tensor(dt)

        weight = self.recurrent_weight * self.recurrent_mask
        candidate = torch.tanh(
            self.input(x_t) + nn.functional.linear(state, weight, self.recurrent_bias)
        )
        tau = self.neuron_tau.to(dtype=x_t.dtype)
        alpha = -torch.expm1(-dt_tensor / tau)
        return state + alpha * (candidate - state)


class FlyRNN(nn.Module):
    """Sequence classifier and embedding model for ``[batch, time, sensor]`` data."""

    def __init__(self, config: FlyRNNConfig) -> None:
        super().__init__()
        self.config = config
        self.cell = FlyRNNCell(config)
        self.readout = nn.Sequential(
            nn.LayerNorm(config.hidden_size * 3),
            nn.Linear(config.hidden_size * 3, config.hidden_size),
            nn.GELU(),
            nn.Linear(config.hidden_size, config.output_size),
        )

    def forward(
        self,
        x: Tensor,
        dt: float | Tensor = 1.0,
        *,
        return_sequence: bool = False,
    ) -> tuple[Tensor, Tensor] | tuple[Tensor, Tensor, Tensor]:
        if x.ndim != 3:
            raise ValueError("x must have shape [batch, time, sensor]")
        if x.shape[-1] != self.config.input_size:
            raise ValueError(
                f"expected {self.config.input_size} sensors, got {x.shape[-1]}"
            )

        state = x.new_zeros((x.shape[0], self.config.hidden_size))
        states = []
        for t in range(x.shape[1]):
            state = self.cell(x[:, t], state, dt)
            states.append(state)
        sequence = torch.stack(states, dim=1)
        embedding = torch.cat(
            [sequence[:, -1], sequence.mean(dim=1), sequence.amax(dim=1)], dim=-1
        )
        logits = self.readout(embedding)
        if return_sequence:
            return logits, embedding, sequence
        return logits, embedding
