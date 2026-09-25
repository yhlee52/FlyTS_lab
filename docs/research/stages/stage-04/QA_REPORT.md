# Stage 04 Independent QA Report

Date: 2026-09-25
Verdict: **PASS**.

## Scope checked

- Exact legacy fly-like graph generation, artifact validation and descriptive statistics.
- Foundation state and parameter contracts, CPU numerical compatibility, format-v1 loading and resume.
- Dense/scatter regression coverage, evaluator-row stability, scope boundaries and research records.

## Evidence

- Focused topology suite: 13 passed.
- Full CPU suite: 68 passed and three CUDA hardware skips.
- Ignored pre-refactor CPU snapshot comparison: bitwise state and parameter order, forward outputs, loss and gradients; strict runtime format-v1 load.
- Committed regressions: five seeded graph edge hashes, state keys/shapes/dtypes, parameter order/count, strict v1 load, bitwise uninterrupted-versus-legacy resume and legacy-versus-explicit evaluator rows.
- Research notebook and governance validators passed; `git diff --check` exited successfully.

## Blockers

- None. Initial QA issued `CONDITIONAL PASS` only because `CURRENT_STATE.md` retained the pre-handoff count of 64 tests. After it was corrected to 68 passed and three skips, QA independently revalidated the notebook and issued final `PASS`.

## Missing verification

- CUDA behavior remains unverified because the environment has a CPU-only PyTorch build and no CUDA device.
- The pre-refactor numerical snapshot is ignored local evidence; the portable committed fixture records structural contracts but not the complete binary snapshot.

## Regression risks

- Focused statistics assertions cover density and degree totals but do not independently freeze every descriptive fraction or weak-component value.
- This verdict establishes compatibility of the extraction only. It does not establish topology benefit, foundation-model quality, transfer or Stage 05 controls.

## Conditions

- None for the Stage 04 result gate. Merge and Stage 05 remain separate user decisions.
