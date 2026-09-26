"""Topology artifact and registered graph builders."""
from .base import GraphArtifact
from .fly_like import build_fly_like
from .controls import build_control
from .stats import graph_statistics, reference_comparison_statistics
from .validation import validate_graph


def build_topology(kind: str, **kwargs) -> GraphArtifact:
    if kind == "fly_like":
        kwargs.pop("control_seed", None)
        graph = build_fly_like(**kwargs)
    elif kind in ("degree_preserving_rewired", "random_sparse"):
        graph = build_control(kind, **kwargs)
    else:
        raise ValueError(f"unknown topology kind {kind!r}; supported: fly_like, degree_preserving_rewired, random_sparse")
    validate_graph(graph)
    return graph


__all__ = ["GraphArtifact", "build_topology", "graph_statistics", "reference_comparison_statistics", "validate_graph"]
