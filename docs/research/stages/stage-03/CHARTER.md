# Stage 03 Charter — Foundation Robustness Evaluator

Status: closed

Execution boundary: user-approved closure without numerical freeze; final independent QA `PASS`.

## Research question

Can one offline deterministic evaluator produce reproducible paired, record-to-domain-macro robustness evidence for FlyTS and a minimal future backbone adapter without touching test or final-held-out data?

## In scope

- Versioned evaluator core, `flyts evaluate-robustness` CLI, FlyTS adapter, raw record rows, compact JSON/CSV/Markdown summaries.
- Reconstruction, permutation, 0/10/30/50% channel dropout, nested unseen/nearest-seen counts, padding, and missing-value controls.
- Synthetic null/sensitivity controls and bounded public development-only calibration candidates, subject to exact public manifest availability.
- Numerical guard, threshold, and uncertainty *candidates* for a separate user decision.

## Out of scope

- Test/final-held-out access, Stage 09 evidence, model or checkpoint changes, new datasets/splits, topology comparison, full pretraining, formal quality/transfer/CUDA claims, Stage 04.
- Final threshold freeze, robustness pass/fail claim, PR merge, and Stage 04 work.

## Inputs

- Latest merged `main` baseline `461f1fc1dc1c809a9486dc36a70e3f942e5d309c` (PR #8).
- `docs/PROJECT_CONSENSUS.md`, `docs/EXPERIMENT_PROTOCOL.md`, `docs/DEVELOPMENT_PLAN.md` Stage 03, Stage 02 `RESULT.md` and `QA_REPORT.md`, `docs/MASKING.md`.
- Public starter corpus exact manifest SHA-256 `e538e9cbf761577740f43f6930ac4653834fdc00f9d0ee567b02b52e2d0d14eb`; local bytes were verified before calibration. A future mismatch is a HOLD, not permission to substitute.

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| Evaluator, CLI, schema, focused tests | `src/flyts/evaluation.py`, `src/flyts/__main__.py`, `schemas/`, `tests/test_evaluation.py` | Implementation Engineer |
| Contract and candidate config | `docs/EVALUATION.md`, `configs/evaluation/robustness-v1.json` | Implementation Engineer |
| Candidate report and raw rows | `reports/robustness/` summary, ignored `outputs/` raw evidence | Research Director with Implementation Engineer |
| Stage records | `docs/research/stages/stage-03/` and research notebook | Research Director |
| Independent candidate QA | `docs/research/stages/stage-03/QA_REPORT.md` | QA Engineer |

## Acceptance criteria

- [x] Identical manifest/checkpoint/config/seed yields identical stable results, fixture hash and deterministic record/domain order — `tests/test_evaluation.py`, ignored `outputs/stage03/eval-seed*/summary.json`.
- [x] Valid originally observed evaluator targets use Smooth L1 `beta=1.0`, with positions→window→manifest record→equal record/domain→equal domain macro; micro and worst domain stay diagnostic — `tests/test_evaluation.py`, `docs/EVALUATION.md`.
- [x] Paired masks/views use the same source record and shared targets; test and final-held-out access fail explicitly — `tests/test_evaluation.py` and evaluator role guards.
- [x] Identity/no-op, order-sensitive, dropout, count, padding and missingness fixtures have focused controls, finite results or explicit undefined status — `tests/test_evaluation.py`; algebraic sensitivity references in the candidate brief are explicitly not executed fixtures.
- [x] Config/result schema versions and manifest/checkpoint/config/fixture hashes are retained; stable results are separate from runtime fields; JSON/CSV/Markdown agree — `schemas/robustness-result-v1.schema.json`, `reports/robustness/calibration-candidate-v1.{json,csv,md}`.
- [x] Focused tests, full pytest, governance/notebook validators and `git diff --check` pass — independent final QA `PASS`; `QA_REPORT.md`.
- [x] Development-only calibration candidate report includes three seeds (`7/17/29`), 400 optimizer steps each, control evidence, 10,000 paired hierarchical bootstrap resamples and 2–3 user options — exact-hash public manifest and `reports/robustness/calibration-candidate-v1.json`.
- [x] Independent remediation QA verified candidate evidence; final independent QA reported `PASS` for the approved no-frozen-threshold closure. Candidate values remain unfrozen; `QA_REPORT.md`, `RESULT.md`.

## User checkpoints

| Decision gate | When to ask | Current approval |
|---|---|---|
| Stage Charter and approved design | Before implementation | `GO`, 2026-09-25 |
| Public manifest unavailable or protected decision change | Before dependent work | `HOLD` as needed |
| Threshold/guard/uncertainty candidate | After candidate report | User `GO — defer freeze`: candidate milestone accepted; settings remain candidate; additional evidence scope pending separate approval |
| Stage closure without numerical freeze | Before final QA | User approved; final QA `PASS`; `RESULT.md` closed |
| Draft PR | After final QA | User approved creation; Research Director executes after QA |
| Merge and Stage 04 | Separate later user gate | not authorized |

## Agent plan

- Research Director integrates requirements and owns user gates.
- Experiment Scientist reviews metric, fixture, aggregation, and calibration evidence read-only.
- Implementation Engineer is the sole tracked-file writer.
- QA Engineer independently re-runs evaluator and candidate checks without tracked edits.
- Distinct metric and QA review reduce leakage and post-hoc threshold risk.

## Budget

```yaml
agent_budget:
  default_mode: single_agent
  max_specialists: 3
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 1
  max_agent_report_words: 700
  recursive_delegation: false
  user_approval_for_expansion: true
```

## Risks and stop conditions

- HOLD if the exact public manifest is absent or mismatched, test/final-held-out is requested, no-op and sensitivity controls overlap, calibration evidence is insufficient, or a metric/split/budget/architecture/acceptance change becomes necessary.
- Development evidence cannot establish foundation quality, transfer, topology advantage or CUDA support.

## User approval

- Decision: `GO` for evaluator/candidate evidence and later closure preparation without numerical freeze.
- Date: 2026-09-25.
- Conditions: all numerical guards, thresholds and uncertainty settings remain `candidate` and unfrozen. Report descriptive metrics only; no robustness pass/fail or final claim. Final independent QA `PASS` closes Stage 03 only within this scope.
