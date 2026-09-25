"""Exact legacy synthetic fly-like graph generation sequence."""
import torch

from .base import GraphArtifact, artifact_from_mask


def build_fly_like(*, hidden_size: int, num_modules: int, num_populations: int,
                   population: torch.Tensor,
                   sparsity: float, reciprocal_fraction: float = 0.20,
                   hub_fraction: float = 0.08, seed: int = 7) -> GraphArtifact:
    if hidden_size <= 1 or not 1 <= num_modules <= hidden_size:
        raise ValueError("invalid hidden_size or num_modules")
    if not 0 <= sparsity < 1 or not 0 <= reciprocal_fraction <= 1 or not 0 <= hub_fraction <= 1:
        raise ValueError("invalid fly_like density/fraction")
    if (population.shape != (hidden_size,) or population.dtype != torch.int64
            or population.device.type != "cpu" or not 1 <= num_populations <= hidden_size
            or bool((population < 0).any()) or bool((population >= num_populations).any())):
        raise ValueError("population must be int64 [hidden_size]")
    n = hidden_size
    generator = torch.Generator().manual_seed(seed)
    module = torch.arange(n) * num_modules // n
    base_density = 1.0 - sparsity
    same_module = module[:, None] == module[None, :]
    probabilities = torch.full((n, n), base_density * 0.55)
    probabilities[same_module] = min(1.0, base_density * 2.25)
    mask = torch.rand((n, n), generator=generator) < probabilities
    reciprocal_candidates = mask & ~mask.T
    add_reverse = (
        torch.rand((n, n), generator=generator) < reciprocal_fraction
    ) & reciprocal_candidates
    mask |= add_reverse.T
    hub_count = max(1, round(n * hub_fraction)) if hub_fraction else 0
    if hub_count:
        hubs = torch.randperm(n, generator=generator)[:hub_count]
        hub_density = min(0.50, max(0.15, base_density * 3.0))
        mask[hubs, :] |= torch.rand((hub_count, n), generator=generator) < hub_density
        mask[:, hubs] |= torch.rand((n, hub_count), generator=generator) < hub_density
    mask.fill_diagonal_(False)
    for target in torch.where(mask.sum(dim=1) == 0)[0].tolist():
        source = (target + 1) % n
        mask[target, source] = True
    parameters = dict(hidden_size=n, num_modules=num_modules,
                      num_populations=num_populations, sparsity=sparsity,
                      reciprocal_fraction=reciprocal_fraction, hub_fraction=hub_fraction)
    return artifact_from_mask(mask.float(), population, module, kind="fly_like",
                              seed=seed, parameters=parameters)
