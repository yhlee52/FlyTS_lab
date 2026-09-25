# Stage 03 Independent QA Report

Date: 2026-09-25
Verdict: **PASS — approved evaluator and candidate deliverables under no-frozen-threshold closure**.

## Scope and acceptance

Independent QA found all eight Charter acceptance criteria satisfied within the user-approved evaluator and development-candidate scope. This verdict does not freeze numerical thresholds, denominator guards, or uncertainty settings and does not certify a robustness pass/fail or foundation-quality claim. The earlier pre-remediation `CONDITIONAL PASS` and remediation candidate `PASS` remain separate historical reviews.

## Evidence reviewed

- Focused evaluator suite: 19 passed, one CUDA hardware skip. Full suite: 55 passed, three CUDA hardware skips. Research notebook and governance validators plus `git diff --check` passed.
- Deterministic paired fixtures, record/position weighting and domain macro, stable ordering, finite/undefined guards, schema and JSON/CSV/Markdown agreement, and raw-to-aggregate provenance were checked against `tests/test_evaluation.py`, `src/flyts/evaluation.py`, and `reports/robustness/calibration-candidate-v1.{json,csv,md}`.
- Development-only sealing: exact public manifest SHA-256 `e538e9cbf761577740f43f6930ac4653834fdc00f9d0ee567b02b52e2d0d14eb`; train/val overlap checked without opening test arrays; `test` and final-held-out roles explicitly rejected. Seeds `7/17/29` used 400 steps and uniformly trained `last.pt`; ignored `outputs/stage03/` holds raw rows and checkpoints.
- Evaluator config SHA-256 `8495082014eb539e64c7671cc9227509b3769c4709a954f5dade71ced09e1211`; evaluator source `e8417668ddb02f8ecf900df40a202e9427ba46f80ddbcf0fb46314f2577574f1`; paired fixture `d48087dac8456d191a277c6e59421798a679e4079ca2e859faa398bde6324f0f`. Base `main`: `461f1fc1dc1c809a9486dc36a70e3f942e5d309c`. Checkpoint and raw-result hashes are in the candidate JSON and Stage 03 `RESULT.md`.

## Limits and disposition

Three interpolation count arms each have only one eligible domain and source record. The order-sensitive algebraic reference is not an executed sensitivity fixture. CUDA is unverified. Three development domains/seeds and candidate intervals cannot justify frozen effect thresholds or generalization claims. The candidate evidence is usable for user review, but numerical freeze remains insufficiently supported. Formal robustness pass/fail requires separately approved reopened calibration and freeze; Draft PR review, merge, and Stage 04 retain their separate gates.
