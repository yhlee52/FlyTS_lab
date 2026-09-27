"""Deterministic Stage 06 corpus structure and missingness report."""
import argparse
from collections import Counter
import json
from pathlib import Path

import numpy as np

from flyts.corpus import safe_path, sha256, verify_corpus


def _count_nonfinite(path, channels):
    array = np.load(path, mmap_mode="r", allow_pickle=False)
    chunk_rows = max(1, 1_000_000 // channels)
    missing = nonfinite = 0
    for start in range(0, len(array), chunk_rows):
        block = array[start:start + chunk_rows]
        missing += int(np.isnan(block).sum())
        nonfinite += int((~np.isfinite(block)).sum())
    return missing, nonfinite


def _duration(seconds):
    seconds = int(seconds)
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    for value, suffix in ((days, "d"), (hours, "h"), (minutes, "m"), (seconds, "s")):
        if value:
            parts.append(f"{value}{suffix}")
    return " ".join(parts) or "0s"


def report(manifest, registry, output, check=False):
    doc = verify_corpus(manifest, registry)
    rows = doc["records"]
    summary = {
        "schema_version": 1,
        "manifest_sha256": sha256(manifest),
        "registry_sha256": sha256(registry),
        "datasets": {},
        "sources": {name: {"archive_sha256": source.get("sha256"),
                            "member_sha256": source.get("member_sha256"),
                            "doi": source.get("doi"), "license": source.get("license")}
                    for name, source in sorted(doc["sources"].items())},
    }
    for dataset in sorted({row["dataset"] for row in rows}):
        subset = [row for row in rows if row["dataset"] == dataset]
        missingness = {}
        for split in ("train", "val", "test"):
            selected = [row for row in subset if row["split"] == split]
            points = sum(row["shape"][0] * row["shape"][1] for row in selected)
            missing = nonfinite = 0
            for row in selected:
                m, nf = _count_nonfinite(safe_path(Path(manifest).parent, row["path"]),
                                         row["shape"][1])
                missing += m
                nonfinite += nf
            missingness[split] = {"points": points, "missing": missing,
                                  "nonfinite": nonfinite,
                                  "missing_rate": missing / points if points else None,
                                  "nonfinite_rate": nonfinite / points if points else None}
        summary["datasets"][dataset] = {
            "domain_id": subset[0].get("domain_id", dataset),
            "domain_family": subset[0].get("domain_family", subset[0]["domain"]),
            "channels": sorted({row["shape"][1] for row in subset}),
            "sampling_seconds": sorted({row["dt"] for row in subset}),
            "purge": {"points": 512, "seconds": 512 * subset[0]["dt"]},
            "records_by_split": dict(sorted(Counter(row["split"] for row in subset).items())),
            "rows_by_split": {split: sum(row["shape"][0] for row in subset
                                         if row["split"] == split)
                              for split in ("train", "val", "test")},
            "entities": sorted({row.get("entity_id", row["group"]) for row in subset}),
            "missingness_by_split": missingness,
        }
    target = Path(output)
    json_bytes = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode("utf-8")
    lines = ["# Stage 06 corpus metadata", "", f"Manifest SHA-256: `{summary['manifest_sha256']}`",
             f"Registry SHA-256: `{summary['registry_sha256']}`", "",
             "| Dataset | Channels | Sampling seconds | Purge after val/test boundary | Train / val / test records | Missing / nonfinite points by split |",
             "|---|---:|---:|---:|---:|---:|"]
    for name, item in summary["datasets"].items():
        counts = item["records_by_split"]
        missing = item["missingness_by_split"]
        point_counts = " / ".join(f"{missing[split]['missing']} / {missing[split]['nonfinite']}"
                                  for split in ("train", "val", "test"))
        purge = item["purge"]
        lines.append(f"| {name} | {item['channels']} | {item['sampling_seconds']} | "
                     f"{purge['points']} points / {_duration(purge['seconds'])} | "
                     f"{counts.get('train', 0)} / {counts.get('val', 0)} / {counts.get('test', 0)} | {point_counts} |")
    md_bytes = ("\n".join(lines) + "\n").encode("utf-8")
    markdown = target.with_suffix(".md")
    if check:
        if not target.exists() or not markdown.exists() or target.read_bytes() != json_bytes or \
                markdown.read_bytes() != md_bytes:
            raise ValueError("Stage 06 report differs from current corpus")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(json_bytes)
        markdown.write_bytes(md_bytes)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--domain-registry", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report(args.manifest, args.domain_registry, args.output, check=args.check)
