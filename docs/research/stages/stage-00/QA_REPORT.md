# Stage 00 Independent QA Report

Date: 2026-09-24

## Verdict

`PASS`. No model, data, checkpoint, export, test, governance, or notebook blocker was reproduced.

## Independent evidence

- Governance validation passed; full test suite: 24 passed and 1 CUDA hardware skip.
- A fresh ignored QA corpus contained 60 records with train/validation/test counts 42/9/9 across three domains. Its manifest hash matched the implementation report, and groups and array hashes were disjoint across splits.
- CPU smoke training reproduced 17,936 parameters, 65/9 train/validation windows, and the report's exact two-epoch losses.
- Epoch-boundary resume reproduced all 29 model tensors bitwise and matched losses exactly.
- Export reloaded without pickle with finite float32 embeddings `[9, 32]`, int64 labels `[9]`, and Unicode dataset identifiers `[9]`; metadata matched test records.
- Installed versions and editable installation metadata matched the baseline report.
- CUDA was unavailable: CPU-only PyTorch build, zero CUDA devices. No provisioning was attempted.
- No source, configuration, architecture, dataset, model-behavior, or evaluation change was found, and no validation claim was strengthened.

## Condition and gaps

- The initial QA condition was to remove stale notebook statements that PyTorch/pytest were absent and that baseline execution had not begun. The Research Director refreshed `CURRENT_STATE.md`; QA reran the notebook checker, governance validator, and `git diff --check`, then confirmed the condition resolved and issued `PASS`.
- QA did not independently reinstall into a second environment or reproduce the implementation-only peak-memory measurement.
- The development plan mentions a frozen probe path. The approved Charter requires embedding export; the full suite covers a fixture-based probe, while no new probe score was claimed.
- Dependency minimums are not fully pinned, so future fresh installations may resolve different versions.

## Evidence paths

- `docs/BASELINE_VALIDATION.md`
- Ignored independent artifacts: `outputs/phase0-baseline/qa/`
