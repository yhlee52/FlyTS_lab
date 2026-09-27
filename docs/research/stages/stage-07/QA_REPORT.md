# Stage 07 Independent QA Report

Date: 2026-09-27

Final verdict: **PASS — provenance remediation re-reviewed**

## Scope

Independent review of the approved conventional-backbone engineering stage. QA
modified no tracked implementation files and used no public corpus, held-out data,
training run or performance evidence.

## Initial passing evidence

- Focused suite: 63 passed, 2 CUDA hardware skips.
- Full suite: 96 passed, 3 CUDA hardware skips.
- Fly format-v1, `graph.*`, topology, initialization and resume regressions pass.
- Fly has 68,760 parameters; dense-leaky selects `H=98` and 68,530; GRU selects
  `H=43` and 68,853. Both baselines are inside the approved five-percent band.
- All arms pass the fixed-mask synthetic forward, finite-gradient, optimizer-update,
  padding, adapter and bitwise two-step-resume checks.
- Dense recurrence has row L1 below one and bounded tau; GRU ignores direct `delta`;
  channel-permutation differences remain below `5e-7` on the QA probe.
- The tracked report contains no loss values or performance ranking. Notebook check
  and `git diff --check` passed; no forbidden artifacts were present.

## Initial blockers

1. Every reported config SHA-256 differs from the corresponding tracked file's
   byte hash on Windows. The generator hashes LF strings, writes CRLF files, and
   `--check` compares newline-normalized text, so invalid byte provenance passes.
2. The initial Charter used the invalid status `approved / active`. The Director
   corrected the record to the single allowed value `active`; QA has not rechecked it.
3. Report source provenance omits modified `src/flyts/training.py` and
   `src/flyts/evaluation.py` even though they affect checkpoint and adapter evidence.

## Remediation and final re-review

- Generate explicit UTF-8/LF bytes, hash exactly the bytes written, and make
  `--check` compare `read_bytes()` against those bytes.
- Bind every report-affecting implementation source, including training and
  evaluation, then regenerate JSON, Markdown and all four configs.
- Add regression coverage that independently hashes tracked config bytes.
- Rerun focused/full suites, report `--check`, governance/notebook validators and
  diff/status checks in the single allowed QA follow-up.

CUDA, real-data behavior, model performance, transfer, robustness pass/fail and
backbone/topology superiority remain `미검증` or out of scope.

DEC-025 authorized one narrow Implementation follow-up. Remediation writes explicit
UTF-8/LF bytes, hashes exactly the config bytes written, compares `read_bytes()` in
`--check`, binds all report-affecting sources, and independently rejects CRLF drift.

Final QA evidence:

- Focused suite: 64 passed, 2 CUDA hardware skips.
- Full suite: 97 passed, 3 CUDA hardware skips.
- All four config byte hashes and all 19 source hashes match the report.
- All six generated artifacts use LF; an independent CRLF mutation is rejected.
- Report `--check`, governance/notebook validators and `git diff --check` pass.
- Model, matcher, initialization, checkpoint and evidence-scope hashes did not drift.
- No corpus, held-out, loss-value, ranking, timing or performance artifact appeared.

CUDA remains unavailable. The PI retains the result gate; merge and Stage 08 remain
separately unauthorized.

## Post-QA integration note

This is a Director integration record, not a second specialist verdict. Draft PR
Linux CI showed that seeded tensor-value bytes differ across operating systems even
though paired shared tensors are bitwise equal within each run. The stable report
now records the actual equality result plus a platform-neutral hash of the ordered
name/shape/dtype/equality transcript. A focused regression enforces this schema;
both Draft PR #13 Linux `pytest` checks pass. Model math, matching, checkpoints and
the independent QA verdict are unchanged.
