"""Descriptive graph statistics; no topology quality claims."""
from .base import GraphArtifact
from .validation import validate_graph


def graph_statistics(graph: GraphArtifact) -> dict:
    validate_graph(graph)
    n = graph.mask.shape[0]
    e = graph.src.numel()
    out_degree = graph.mask.sum(0).int().tolist()
    in_degree = graph.mask.sum(1).int().tolist()
    reverse = int(graph.mask[graph.src, graph.dst].sum().item())
    within = int((graph.module[graph.src] == graph.module[graph.dst]).sum().item())
    parent = list(range(n))

    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for src, dst in zip(graph.src.tolist(), graph.dst.tolist()):
        parent[root(src)] = root(dst)
    density = e / (n * (n - 1))
    return dict(nodes=n, edges=e, density=density, sparsity=1-density,
                in_degree=in_degree, out_degree=out_degree,
                reciprocal_edge_fraction=reverse/e,
                within_module_edge_fraction=within/e,
                weak_components=len({root(i) for i in range(n)}))
