"""Topology artifact and registered graph builders."""
from .base import GraphArtifact
from .fly_like import build_fly_like
from .stats import graph_statistics
from .validation import validate_graph


def build_topology(kind: str, **kwargs) -> GraphArtifact:
    if kind != "fly_like":
        raise ValueError(f"unknown topology kind {kind!r}; supported: fly_like")
    graph = build_fly_like(**kwargs)
    validate_graph(graph)
    return graph


__all__ = ["GraphArtifact", "build_topology", "graph_statistics", "validate_graph"]
