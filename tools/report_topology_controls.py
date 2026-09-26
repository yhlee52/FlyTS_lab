"""Reproduce or check the small Stage 05 structural evidence report."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from flyts.topology import build_topology, graph_statistics, reference_comparison_statistics


SOURCE_PATHS = (
    "src/flyts/topology/controls.py",
    "src/flyts/topology/__init__.py",
    "src/flyts/topology/stats.py",
    "src/flyts/foundation.py",
    "src/flyts/training.py",
    "src/flyts/evaluation.py",
    "configs/topology/stage05-controls.json",
    "tools/report_topology_controls.py",
)


def validate_source_commit(source_commit):
    for path in SOURCE_PATHS:
        result = subprocess.run(["git", "cat-file", "-e", f"{source_commit}:{path}"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        if result.returncode:
            raise SystemExit(f"source commit {source_commit} lacks {path}")


def source_hashes():
    return {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in SOURCE_PATHS}


def make_report(source_commit):
    config = json.loads((ROOT / "configs/topology/stage05-controls.json").read_text(encoding="utf-8"))
    n = config["hidden_size"]
    population = torch.arange(n) * config["num_populations"] // n
    kwargs = dict(hidden_size=n, num_modules=config["num_modules"],
                  num_populations=config["num_populations"], population=population,
                  sparsity=1-config["density"], seed=config["topology_seed"])
    kinds = ("fly_like", "degree_preserving_rewired", "random_sparse")
    graphs = {kind: build_topology(kind, **kwargs,
                                  control_seed=config["topology_control_seed"])
              for kind in kinds}
    provenance = dict(base_commit=config["base_commit"], source_commit=source_commit,
                      source_sha256=source_hashes(), python=sys.version.split()[0],
                      torch=torch.__version__, device="cpu",
                      reproduction=(f"git checkout {source_commit} && python "
                                    f"tools/report_topology_controls.py --source-commit {source_commit}"))
    arms = {}
    for kind, graph in graphs.items():
        arms[kind] = dict(kind=graph.kind, schema_version=graph.schema_version,
                          content_hash=graph.content_hash, reference_seed=config["topology_seed"],
                          control_seed=(None if kind == "fly_like" else config["topology_control_seed"]),
                          resolved_seed=graph.seed, parameters=dict(graph.parameters),
                          statistics=graph_statistics(graph),
                          reference_comparison=reference_comparison_statistics(graph, graphs["fly_like"]))
    return dict(config=config, provenance=provenance, arms=arms)


def render_markdown(report):
    lines = ["# Stage 05 topology controls", "",
             "Synthetic structural evidence only; no performance or biological claim.", "",
             f"Source commit: `{report['provenance']['source_commit']}`. Reproduce: `{report['provenance']['reproduction']}`.",
             "", "| Kind | Edges | Components | Hash | Retained fraction | Jaccard | Zero outdegree |",
             "|---|---:|---:|---|---:|---:|---:|"]
    for kind, arm in report["arms"].items():
        stats = arm["statistics"]
        compare = arm["reference_comparison"]
        lines.append(f"| {kind} | {stats['edges']} | {stats['weak_components']} | `{arm['content_hash']}` | {compare['retained_edge_fraction']:.6f} | {compare['edge_jaccard']:.6f} | {stats['zero_outdegree_nodes']} |")
    lines += ["", "The retained fractions and Jaccard values are descriptive; they were not used to select graphs.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--source-commit")
    args = parser.parse_args()
    json_path = ROOT / "reports/topology/stage05-controls.json"
    source_commit = args.source_commit
    if args.check and source_commit is None:
        source_commit = json.loads(json_path.read_text(encoding="utf-8"))["provenance"]["source_commit"]
    if source_commit is None:
        raise SystemExit("--source-commit is required when writing the report")
    validate_source_commit(source_commit)
    report = make_report(source_commit)
    outputs = {ROOT / "reports/topology/stage05-controls.json":
               json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
               ROOT / "reports/topology/stage05-controls.md": render_markdown(report)}
    for path, content in outputs.items():
        if args.check:
            if path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"report differs: {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
    print("Stage 05 report matches" if args.check else "Stage 05 report written")


if __name__ == "__main__":
    main()
