# Stage 05 Independent QA Report

Date: 2026-09-26
Verdict: **PASS**.

## Scope checked

- Exact structural contracts for `fly_like`, `degree_preserving_rewired`, and
  `random_sparse`, including deterministic seeds, annotations, degree/component
  guards, fixed attempts, global RNG isolation, and descriptive-only overlap.
- Foundation parameter/initialization parity, dense/scatter finite CPU one-step,
  format-v1 checkpoint compatibility, graph provenance and mismatch rejection.
- Tracked report source attribution, byte-stable regeneration, research governance,
  forbidden scope, and absence of data/performance artifacts.

## Evidence

- Focused suite: 60 passed and two CUDA hardware skips.
- Full suite: 76 passed and three CUDA hardware skips.
- All 15 dtype, shape, and value corruptions across the five graph buffers were
  rejected; strict legacy v1 load, cross-topology rejection, resume, evaluator,
  Stage 04 golden/state/parameter contracts, paired initialization, and finite
  dense/scatter one-step checks passed.
- Independent synthetic resume confirmed that both `run.json` and `last.pt` record
  the actual `--resume` and explicit `--epochs 2` invocation.
- The report records 613 edges per arm; rewiring accepted 6,130 swaps in 11,235
  proposals and random sparse accepted candidate 1. Overlap/Jaccard are descriptive.
- `tools/report_topology_controls.py --check` passed; recorded source hashes match
  source commit `ce99704`. Governance/notebook validators, `git diff --check`, and
  final clean `git status` passed on QA handoff HEAD `b926897`.

## Prior blockers and remediation

- Initial QA `FAIL`: report incorrectly named base commit `944f8ed` as the source.
  Remediation separated base/source commits, verifies committed source paths and
  hashes, and records a valid checkout+generation command.
- First follow-up `FAIL`: training provenance omitted resume, epoch override, and
  development-only CLI flags. Remediation added a complete argv builder and focused
  regression test. DEC-020 authorized the final bounded QA follow-up.

## Missing verification

- CUDA, held-out data, topology performance, robustness, transfer, and biological
  mechanism remain outside the approved Stage 05 scope and unverified.

## Regression risks

- Resuming from `run/last.pt` overwrites that input checkpoint. The recorded command
  accurately captures the invocation, but later exact replay requires an archived
  copy of the pre-resume checkpoint.

## Conditions

- None for the Stage 05 result gate. Merge and Stage 06 remain separately gated.
