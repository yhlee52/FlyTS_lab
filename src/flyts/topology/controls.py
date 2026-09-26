"""Deterministic structural controls for the synthetic fly-like reference."""
import hashlib

import torch

from .base import GraphArtifact, artifact_from_mask
from .fly_like import build_fly_like
from .stats import weak_component_count


def resolved_control_seed(kind: str, control_seed: int) -> int:
    if isinstance(control_seed, bool) or not isinstance(control_seed, int):
        raise ValueError("control topology requires an explicit integer topology_control_seed")
    namespace = f"flyts-topology-control-v1/{kind}/{control_seed}".encode("ascii")
    return int.from_bytes(hashlib.sha256(namespace).digest()[:8], "big") & ((1 << 63) - 1)


def build_control(kind: str, *, control_seed: int | None = None, **kwargs) -> GraphArtifact:
    seed = resolved_control_seed(kind, control_seed)
    reference = build_fly_like(**kwargs)
    n, e = reference.mask.shape[0], reference.src.numel()
    generator = torch.Generator().manual_seed(seed)
    components = weak_component_count(reference.mask)
    parameters = dict(reference.parameters, reference_seed=reference.seed,
                      control_seed=control_seed)
    if kind == "degree_preserving_rewired":
        target, limit = 10 * e, 200 * e
        original = set(zip(reference.src.tolist(), reference.dst.tolist()))
        edges = list(original)
        # Canonical initial edge order avoids set-iteration dependence.
        edges.sort(key=lambda edge: (edge[1], edge[0]))
        present = set(edges)
        accepted = 0
        for attempts in range(1, limit + 1):
            i, j = torch.randint(e, (2,), generator=generator).tolist()
            if i == j:
                continue
            a, b = edges[i]
            c, d = edges[j]
            first, second = (a, d), (c, b)
            if (a == c or b == d or a == d or c == b or first in present
                    or second in present or first == second):
                continue
            candidate = present - {(a, b), (c, d)} | {first, second}
            mask = torch.zeros((n, n), dtype=torch.float32)
            for src, dst in candidate:
                mask[dst, src] = 1
            if weak_component_count(mask) != components:
                continue
            present = candidate
            edges[i], edges[j] = first, second
            accepted += 1
            if accepted == target:
                break
        if accepted != target:
            raise ValueError(f"rewiring failed: accepted {accepted}/{target} swaps in {attempts}/{limit} attempts")
        if present == original:
            raise ValueError("rewiring failed: final edge set equals reference")
        parameters.update(target_swaps=target, max_attempts=limit,
                          accepted_swaps=accepted, attempts=attempts)
    elif kind == "random_sparse":
        if e > n * (n - 1):
            raise ValueError("random_sparse cannot fit reference edge count")
        reference_in, reference_out = reference.mask.sum(1), reference.mask.sum(0)
        for candidate_index in range(1, 257):
            choices = torch.randperm(n * (n - 1), generator=generator)[:e]
            src = choices // (n - 1)
            dst = choices % (n - 1)
            dst += (dst >= src).long()
            mask = torch.zeros((n, n), dtype=torch.float32)
            mask[dst, src] = 1
            if (bool((mask.sum(1) > 0).all()) and weak_component_count(mask) == components
                    and not (torch.equal(mask.sum(1), reference_in)
                             and torch.equal(mask.sum(0), reference_out))):
                break
        else:
            raise ValueError("random_sparse failed: no valid candidate in 256 attempts")
        parameters.update(max_candidates=256, candidate_attempts=candidate_index)
    else:
        raise ValueError(f"unknown topology kind {kind!r}")
    return artifact_from_mask(mask, reference.population, reference.module,
                              kind=kind, seed=seed, parameters=parameters)
