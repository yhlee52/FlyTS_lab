"""Build a Stage 03 candidate brief from three ignored development evaluator runs."""
import argparse
from collections import defaultdict
import csv
import json
import math
from pathlib import Path

import numpy as np

from flyts.corpus import sha256


EXPECTED_MANIFEST = "e538e9cbf761577740f43f6930ac4653834fdc00f9d0ee567b02b52e2d0d14eb"
POSITION_METRICS = {"reconstruction", "dropout", "channel_count", "missing"}
SEEDS = (7, 17, 29)
RESAMPLES = 10_000
REPO_ROOT = Path(__file__).resolve().parents[1]


def portable_path(path):
    """Never publish a workstation-absolute or user-home path in Git evidence."""
    resolved = Path(path).resolve()
    if not resolved.is_relative_to(REPO_ROOT):
        raise ValueError("candidate evidence path must stay inside the repository")
    return resolved.relative_to(REPO_ROOT).as_posix()


def _mean(rows, field, metric):
    usable = [row for row in rows if row[field] is not None]
    if not usable:
        return None
    if metric in POSITION_METRICS:
        counts = [row["target_count"] for row in usable]
        if any(type(count) is not int or count < 1 for count in counts):
            raise ValueError("invalid position count in calibration raw row")
        return sum(row[field] * count for row, count in zip(usable, counts)) / sum(counts)
    return sum(row[field] for row in usable) / len(usable)


def collapse_records(raw_rows):
    groups = defaultdict(list)
    for row in raw_rows:
        groups[(row["metric"], row["arm"], row["domain"], row["record_id"])].append(row)
    cells = {}
    for (metric, arm, domain, record), rows in groups.items():
        if all("baseline" in row and "corrupted" in row for row in rows):
            cells[(metric, arm, domain, record)] = (
                _mean(rows, "baseline", metric), _mean(rows, "corrupted", metric))
        else:
            value = _mean(rows, "value", metric)
            if value is not None:
                cells[(metric, arm, domain, record)] = (value,)
    return cells


def bootstrap_interval(all_cells, metric, arm, seed=3007, resamples=RESAMPLES):
    """Paired seed/domain/source-record hierarchical percentile candidate."""
    keys = [{(domain, record) for m, a, domain, record in cells if m == metric and a == arm}
            for cells in all_cells]
    common = set.intersection(*keys)
    domains = sorted({domain for domain, _ in common})
    if not domains:
        return None
    records = {domain: sorted(record for d, record in common if d == domain) for domain in domains}
    paired = len(all_cells[0][(metric, arm, domains[0], records[domains[0]][0])]) == 2
    rng = np.random.default_rng(seed)
    estimates = []
    for _ in range(resamples):
        chosen_seeds = rng.integers(0, len(all_cells), len(all_cells))
        chosen_domains = rng.integers(0, len(domains), len(domains))
        domain_values = []
        for domain_index in chosen_domains:
            domain = domains[int(domain_index)]
            domain_records = records[domain]
            chosen_records = rng.integers(0, len(domain_records), len(domain_records))
            values = [all_cells[int(seed_index)][(metric, arm, domain,
                      domain_records[int(record_index)])]
                      for seed_index in chosen_seeds for record_index in chosen_records]
            domain_values.append(tuple(sum(value[j] for value in values)/len(values)
                                       for j in range(2 if paired else 1)))
        macro = tuple(sum(value[j] for value in domain_values)/len(domain_values)
                      for j in range(2 if paired else 1))
        if paired:
            if abs(macro[0]) < 1e-8:
                continue
            estimate = (macro[1] - macro[0])/abs(macro[0])
        else:
            estimate = macro[0]
        if math.isfinite(estimate):
            estimates.append(estimate)
    if not estimates:
        return {"status": "undefined_small_denominator", "valid_resamples": 0}
    low, high = np.quantile(estimates, [0.025, 0.975]).tolist()
    return {"status": "candidate", "method": "paired hierarchical percentile bootstrap",
            "level": 0.95, "requested_resamples": resamples,
            "valid_resamples": len(estimates), "lower": low, "upper": high,
            "domains": len(domains), "records_by_domain": {d: len(records[d]) for d in domains}}


def build_candidate(run_dirs, output):
    if len(run_dirs) != 3:
        raise ValueError("exactly three development runs are required")
    summaries, raw, provenance = [], [], []
    for expected_seed, run_dir in zip(SEEDS, map(Path, run_dirs)):
        summary_path = run_dir / "summary.json"
        raw_path = run_dir / "records.jsonl"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines()]
        if summary["status"] != "candidate" or summary["stable"]["provenance"]["split"] != "val":
            raise ValueError("candidate requires validation-only evaluator runs")
        p = summary["stable"]["provenance"]
        if p["manifest_sha256"] != EXPECTED_MANIFEST or p["checkpoint_training"]["seed"] != expected_seed or p["checkpoint_training"]["optimizer_steps"] != 400:
            raise ValueError("candidate run has wrong manifest, seed or compute budget")
        if p["checkpoint_training"]["parameter_count"] != 17936:
            raise ValueError("candidate run parameter count differs")
        if not rows or any(not math.isfinite(row["value"]) for row in rows if row["value"] is not None):
            raise ValueError("missing or non-finite development raw rows")
        training_config_path = (REPO_ROOT /
                                f"configs/evaluation/calibration-train-seed{expected_seed}.json")
        training_config = json.loads(training_config_path.read_text(encoding="utf-8"))
        train_run_path = run_dir.parent / f"seed{expected_seed}" / "run.json"
        train_run = json.loads(train_run_path.read_text(encoding="utf-8"))
        if train_run["config"] != training_config or train_run["manifest_sha256"] != EXPECTED_MANIFEST:
            raise ValueError("training config/run provenance mismatch")
        summaries.append(summary)
        raw.append(rows)
        provenance.append({"seed": expected_seed, "summary": portable_path(summary_path),
                           "summary_sha256": sha256(summary_path), "raw": portable_path(raw_path),
                           "raw_sha256": sha256(raw_path), "checkpoint_sha256": p["checkpoint_sha256"],
                           "training_config": portable_path(training_config_path),
                           "training_config_sha256": sha256(training_config_path),
                           "training_run_sha256": sha256(train_run_path),
                           "batch_size": training_config["batch_size"],
                           "sample_exposure": training_config["batch_size"] * 400,
                           "config_sha256": p["config_sha256"],
                           "evaluator_source_sha256": p["evaluator_source_sha256"],
                           "git_commit": p["git_commit"]})
    fixture_hashes = {summary["stable"]["fixture_sha256"] for summary in summaries}
    source_hashes = {p["evaluator_source_sha256"] for p in provenance}
    if len(fixture_hashes) != 1 or len(source_hashes) != 1:
        raise ValueError("paired seeds must use identical fixture and evaluator source")
    all_cells = [collapse_records(rows) for rows in raw]
    keys = sorted({(row["metric"], row["arm"]) for rows in raw for row in rows})
    results = []
    for index, (metric, arm) in enumerate(keys):
        by_seed = [next((row for row in summary["stable"]["results"]
                         if row["metric"] == metric and row["arm"] == arm), None)
                   for summary in summaries]
        if any(row is None for row in by_seed):
            continue
        values = [row["domain_macro"] for row in by_seed]
        defined = [value for value in values if value is not None]
        interval = bootstrap_interval(all_cells, metric, arm, 3007 + index)
        eligible_records = interval.get("records_by_domain", {}) if interval else {}
        eligible_domains = len(eligible_records)
        min_records = min(eligible_records.values()) if eligible_records else 0
        coverage = ("single_domain_single_record" if eligible_domains == 1 and min_records == 1
                    else "limited_domain_or_record" if eligible_domains < 3 or min_records < 2
                    else "development_only")
        results.append({"metric": metric, "arm": arm,
                        "domain_macro_by_seed": dict(zip(map(str, SEEDS), values)),
                        "domains_by_seed": dict(zip(map(str, SEEDS), [row["domains"] for row in by_seed])),
                        "mean": sum(defined)/len(defined) if defined else None,
                        "std": float(np.std(defined, ddof=1)) if len(defined) > 1 else None,
                        "interval": interval,
                        "eligible_domain_count": eligible_domains,
                        "eligible_source_records_by_domain": eligible_records,
                        "eligible_source_record_count": sum(eligible_records.values()),
                        "coverage_status": coverage,
                        "records_by_seed": dict(zip(map(str, SEEDS), [row["records"] for row in by_seed]))})
    identity = [r["mean"] for r in results if r["metric"] == "permutation" and r["arm"] == "identity"]
    dropout_zero = [r["mean"] for r in results if r["metric"] == "dropout" and r["arm"] == "0%"]
    padding = [r["mean"] for r in results if r["metric"] == "padding" and r["mean"] is not None]
    null_max = max(abs(value) for value in identity + dropout_zero + padding if value is not None)
    # Arithmetic references only: these were not run as empirical fixtures.
    permutation_control = 1 - 10/14  # [1,2,3] versus [3,2,1]
    degradation_control = (2 - 1)/1
    gap = max(0.0, permutation_control - null_max)
    thresholds = {name: null_max + fraction*gap
                  for name, fraction in (("strict", .01), ("balanced", .05), ("lenient", .10))}
    baselines = [abs(row["baseline"]) for rows in raw for row in rows
                 if "baseline" in row and math.isfinite(row["baseline"])]
    report = {
        "schema_version": 1, "status": "candidate", "decision_gate": "HOLD",
        "user_decision": "GO — defer freeze", "candidate_milestone": "accepted",
        "additional_evidence_scope": "requires separate user approval",
        "manifest_sha256": EXPECTED_MANIFEST, "split": "val",
        "domains": sorted({row["domain"] for rows in raw for row in rows}),
        "excluded_splits": ["test"], "excluded_domain_roles": ["final-held-out"],
        "seeds": list(SEEDS), "optimizer_steps_per_seed": 400,
        "fixture_sha256": next(iter(fixture_hashes)), "runs": provenance,
        "raw_rows_by_seed": dict(zip(map(str, SEEDS), map(len, raw))),
        "metric_results": results,
        "controls": {"executed_identity_permutation": identity,
                     "executed_zero_dropout": dropout_zero,
                     "executed_padding_domain_macro": padding,
                     "formula_references_not_executed_fixtures": {
                         "order_sensitive_1_minus_cosine": {
                             "formula": "1 - dot([1,2,3],[3,2,1])/(sqrt(14)*sqrt(14))",
                             "value": permutation_control},
                         "loss_degradation": {"formula": "(2-1)/abs(1)",
                                              "value": degradation_control}},
                     "unit_test_guards": ["near-zero norm undefined", "zero denominator undefined"]},
        "candidate_numerical_guards": {"current_config_floor": 1e-8,
                                        "minimum_observed_absolute_baseline": min(baselines),
                                        "options": {"low_floor": 1e-8, "medium_floor": 1e-7, "high_floor": 1e-6},
                                        "direction": "higher floor marks more relative changes undefined; it is the stricter denominator guard"},
        "candidate_thresholds": {"permutation_formula_gap_options": thresholds,
                                 "effect_thresholds": "insufficient independent controls; no numeric freeze candidate",
                                 "selection_impact": "strict risks false rejection from numerical jitter; lenient risks accepting material drift",
                                 "limitation": "gap uses an algebraic order-sensitive reference, not an executed sensitivity fixture"},
        "candidate_uncertainty": {"method": "paired hierarchical percentile bootstrap",
                                  "level": 0.95, "resamples": RESAMPLES,
                                  "units": ["seed", "domain", "source-record"],
                                  "options": ["hierarchical percentile", "domain-only percentile", "defer freeze"]},
        "limitations": ["three development domains and three seeds; energy and transport have one validation record each",
                        "some channel-count arms have only one eligible domain and one source record; their bootstrap interval cannot establish cross-domain uncertainty or justify freeze",
                        "candidate thresholds are not formal model-quality or final-test evidence",
                        "public development corpus is reused across threshold candidates"],
        "recommendation": "defer threshold freeze (accepted by user); retain candidate controls and intervals",
        "experiment_scientist": "Reproducibility and aggregation structure are suitable for candidate evidence; independent numerical freeze is not supported by the available controls/coverage.",
        "qa_candidate_evidence": {"verdict": "CONDITIONAL PASS (pre-remediation)",
                                  "scope": "implementation and original candidate report",
                                  "confirmed": "seed7 raw-to-aggregate agreement; 31 arms and 10,000 intervals; JSON/CSV/Markdown numeric agreement; focused 18 pass/1 CUDA skip and full 54 pass/3 CUDA skips",
                                  "limitations": "portable provenance, algebraic-reference wording, floor labels and sparse count-arm coverage required remediation; later remediation QA is recorded separately"},
        "remediation_qa": {"verdict": "PASS", "scope": "candidate evidence remediation",
                           "finding": "candidate evidence usable for user review; threshold, guard and uncertainty freeze evidence insufficient",
                           "stage_gate": "open; this is not Stage 03 final QA or closure"},
        "post_remediation_self_validation": "Implementation self-check: focused 19 passed/1 CUDA skip; full 55 passed/3 CUDA skips; governance and notebook validators and git diff --check passed. This is not independent QA."
    }
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "calibration-candidate-v1.json"
    csv_path = output / "calibration-candidate-v1.csv"
    md_path = output / "calibration-candidate-v1.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        fields = ("metric", "arm", "mean", "std", "ci_lower", "ci_upper", "valid_resamples",
                  "eligible_domain_count", "eligible_source_record_count", "eligible_records_by_domain",
                  "coverage_status", "candidate_status", "candidate_milestone", "remediation_qa_verdict", "freeze_evidence")
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in results:
            interval = row["interval"] or {}
            writer.writerow({"metric": row["metric"], "arm": row["arm"],
                             "mean": row["mean"], "std": row["std"],
                             "ci_lower": interval.get("lower"), "ci_upper": interval.get("upper"),
                             "valid_resamples": interval.get("valid_resamples"),
                             "eligible_domain_count": row["eligible_domain_count"],
                             "eligible_source_record_count": row["eligible_source_record_count"],
                             "eligible_records_by_domain": json.dumps(row["eligible_source_records_by_domain"], sort_keys=True),
                             "coverage_status": row["coverage_status"],
                             "candidate_status": "candidate", "candidate_milestone": "accepted",
                             "remediation_qa_verdict": "PASS",
                             "freeze_evidence": "insufficient"})
    lines = ["# Stage 03 calibration candidate — GO to defer freeze; HOLD additional scope", "",
             f"Manifest: `{EXPECTED_MANIFEST}`; split: `val`; seeds: `7/17/29`; 400 steps each.",
             "User accepted the candidate evidence milestone. Threshold, numerical guard and uncertainty settings remain candidate; additional evidence needs separate approval.",
             "Test and final-held-out were excluded. All values and options are candidate only.", "",
             "| Metric | Arm | Mean domain macro | 95% candidate interval | Eligible domains / source records | Coverage |",
             "|---|---|---:|---:|---|---|"]
    for row in results:
        interval = row["interval"] or {}
        value = "undefined" if row["mean"] is None else f"{row['mean']:.8g}"
        ci = (f"[{interval['lower']:.8g}, {interval['upper']:.8g}]"
              if "lower" in interval else "undefined")
        coverage = ", ".join(f"{domain}:{count}" for domain, count in
                             row["eligible_source_records_by_domain"].items())
        lines.append(f"| {row['metric']} | {row['arm']} | {value} | {ci} | {row['eligible_domain_count']} / {row['eligible_source_record_count']} ({coverage}) | {row['coverage_status']} |")
    lines += ["", "## Controls and decision", "",
              f"Identity permutation: {identity}; zero dropout: {dropout_zero}; padding null maxima: {null_max:.8g}.",
              f"Algebraic sanity references only (not executed fixtures): order-sensitive 1-cosine = {permutation_control:.8g} from [1,2,3] vs [3,2,1]; loss degradation = {degradation_control:.8g} from (2-1)/abs(1).",
              f"Permutation formula-gap candidate thresholds: {thresholds}. Numerical denominator floors: low 1e-8 / medium 1e-7 / high 1e-6; higher floor is the stricter guard and marks more relative results undefined.",
              "Effect thresholds lack independent calibration controls; user accepted the recommendation to defer freeze.",
              "Bootstrap: paired seed/domain/source-record, 10,000 resamples, 95% percentile candidate intervals.",
              "Several count arms have only one eligible domain and one source record; those intervals cannot establish cross-domain uncertainty or justify freeze.",
              "Experiment Scientist: reproducibility/aggregation suitable for candidate evidence; numerical freeze unsupported.",
              "QA history: pre-remediation CONDITIONAL PASS. Remediation QA: PASS; candidate evidence is usable for user review. Threshold/guard/uncertainty freeze evidence remains insufficient. This is not Stage 03 final QA or closure.",
              "Implementation self-check after remediation: focused 19 passed/1 CUDA skip; full 55 passed/3 CUDA skips; governance/notebook/diff checks passed. This is not independent QA.",
              "Raw rows and checkpoints remain under ignored `outputs/stage03/`."]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", nargs=3, required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = build_candidate(args.runs, args.output)
    print(json.dumps({"status": report["status"], "metrics": len(report["metric_results"]),
                      "decision_gate": report["decision_gate"]}))


if __name__ == "__main__":
    main()
