"""Structural and content checks for a graph artifact."""
import torch

from .base import GraphArtifact, SCHEMA_VERSION, TENSOR_FIELDS, graph_hash


def validate_graph(graph: GraphArtifact) -> None:
    if tuple(record.name for record in graph._records) != TENSOR_FIELDS:
        raise ValueError("graph tensor field order mismatch")
    expected_dtypes = ("float32", "int64", "int64", "int64", "int64", "int64", "float32")
    if tuple(record.dtype for record in graph._records) != expected_dtypes:
        raise ValueError("graph tensor dtype mismatch")
    n = graph.mask.shape[0]
    if graph.schema_version != SCHEMA_VERSION or graph.direction != "src_to_dst":
        raise ValueError("unsupported graph schema/direction")
    if graph.mask.shape != (n, n) or graph.mask.dtype != torch.float32 or n < 2:
        raise ValueError("mask must be float32 [N,N], N >= 2")
    for value, dtype, shape in ((graph.mask, torch.float32, (n, n)),
                                (graph.src, torch.int64, (graph.src.numel(),)),
                                (graph.dst, torch.int64, (graph.src.numel(),)),
                                (graph.population, torch.int64, (n,)),
                                (graph.module, torch.int64, (n,)),
                                (graph.edge_type, torch.int64, (graph.src.numel(),)),
                                (graph.degree, torch.float32, (n,))):
        if value.device.type != "cpu" or not value.is_contiguous() or value.dtype != dtype or value.shape != shape:
            raise ValueError("graph tensors must have canonical CPU contiguous dtype/shape")
    if not torch.all((graph.mask == 0) | (graph.mask == 1)) or torch.diagonal(graph.mask).any():
        raise ValueError("mask must be binary without self loops")
    if graph.population.min() < 0 or graph.module.min() < 0:
        raise ValueError("population/module assignments must be nonnegative")
    if graph.population.max() >= graph.parameters["num_populations"]:
        raise ValueError("population assignment out of range")
    if graph.module.max() >= graph.parameters["num_modules"]:
        raise ValueError("module assignment out of range")
    dst, src = graph.mask.nonzero(as_tuple=True)
    if not torch.equal(graph.dst, dst) or not torch.equal(graph.src, src):
        raise ValueError("edges must match mask in lexicographic (dst,src) order")
    if not torch.all(graph.mask.sum(1) > 0):
        raise ValueError("every node needs an incoming edge")
    count = graph.parameters["num_populations"]
    if not torch.equal(graph.edge_type, graph.population[dst] * count + graph.population[src]):
        raise ValueError("edge_type inconsistent with population")
    if not torch.equal(graph.degree, graph.mask.sum(1).clamp_min(1)):
        raise ValueError("degree inconsistent with mask")
    expected = graph_hash(graph._records, kind=graph.kind,
                          direction=graph.direction, seed=graph.seed,
                          schema_version=graph.schema_version, parameters=graph.parameters)
    if graph.content_hash != expected:
        raise ValueError("graph content hash mismatch")
