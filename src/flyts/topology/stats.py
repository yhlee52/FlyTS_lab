"""Descriptive graph statistics; no topology quality claims."""
import torch
from .base import GraphArtifact
from .validation import validate_graph


def weak_component_count(mask: torch.Tensor) -> int:
    n = mask.shape[0]
    parent = list(range(n))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    dst, src = mask.nonzero(as_tuple=True)
    for source, target in zip(src.tolist(), dst.tolist()):
        parent[root(source)] = root(target)
    return len({root(i) for i in range(n)})


def graph_statistics(graph: GraphArtifact) -> dict:
    validate_graph(graph)
    n = graph.mask.shape[0]
    e = graph.src.numel()
    out_degree = graph.mask.sum(0).int().tolist()
    in_degree = graph.mask.sum(1).int().tolist()
    reverse = int(graph.mask[graph.src, graph.dst].sum().item())
    within = int((graph.module[graph.src] == graph.module[graph.dst]).sum().item())
    populations = graph.parameters["num_populations"]
    pair = torch.bincount(graph.edge_type, minlength=populations**2).reshape(populations, populations)
    module = graph.module
    out_module = torch.bincount(module[graph.src], minlength=graph.parameters["num_modules"])
    in_module = torch.bincount(module[graph.dst], minlength=graph.parameters["num_modules"])
    modularity = within / e - (out_module.double() * in_module.double()).sum().item() / e**2
    density = e / (n * (n - 1))
    return dict(nodes=n, edges=e, density=density, sparsity=1-density,
                in_degree=in_degree, out_degree=out_degree,
                reciprocal_edge_fraction=reverse/e,
                within_module_edge_fraction=within/e,
                weak_components=weak_component_count(graph.mask),
                zero_outdegree_nodes=sum(value == 0 for value in out_degree),
                population_pair_edge_counts=pair.tolist(),
                directed_module_modularity=modularity)


def reference_comparison_statistics(graph: GraphArtifact, reference: GraphArtifact) -> dict:
    validate_graph(graph)
    validate_graph(reference)
    if graph.mask.shape != reference.mask.shape:
        raise ValueError("comparison graphs require identical node count")
    intersection = int((graph.mask * reference.mask).sum().item())
    e, ref_e = graph.src.numel(), reference.src.numel()
    return dict(edge_overlap=intersection, retained_edge_fraction=intersection/ref_e,
                edge_jaccard=intersection/(e+ref_e-intersection),
                in_degree_l1=int((graph.mask.sum(1)-reference.mask.sum(1)).abs().sum().item()),
                out_degree_l1=int((graph.mask.sum(0)-reference.mask.sum(0)).abs().sum().item()))
