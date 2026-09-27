# Stage 08 Charter — FlyTS-Mini Operational Pilot

Status: closed

Closure: independent QA `PASS`; PI result `GO` on 2026-09-28.

## Research question

Can the four preregistered Stage 09 candidate arms complete one identical,
small-budget public-corpus path from multi-domain pretraining through validation,
checkpoint selection, resume, common evaluation, provenance, resource measurement
and reporting without held-out leakage or arm-specific exceptions?

## In scope

- Appliances and Beijing pretraining; Bike development-held-out validation-only
  evaluation; exact Stage 06 manifest and role registry.
- Full operational runs for `fly_like`, `degree_preserving_rewired`,
  `random_sparse` and GRU, plus a short dense-leaky diagnostic.
- One seed, paired data/mask fixtures, validation-only checkpoint selection,
  epoch-boundary resume, common evaluator, exact provenance, CPU timing/RSS and
  deterministic pilot reporting.
- Minimal trainer/evaluator/runner changes and tests required to exercise the
  approved path.

## Out of scope

- Final-held-out Electricity arrays or model outputs, Stage 09 work, final-test
  access, additional seeds, hyperparameter search or result-driven reruns.
- Topology/backbone superiority, robustness pass/fail, foundation quality,
  transfer, CUDA, semiconductor suitability or formal performance claims.
- Frozen probes, detailed latency benchmarking, numerical-threshold freeze,
  checkpoint/corpus format changes and a new training framework.

## Inputs

- GitHub `main` merge commit `34b83c29d8a5588158d1e4abe420bfc8cbdf5e68`.
- Stage 06 manifest `44bafe48196a4afd096e387dc672cad128d390ab7e5b413ea6cbeadf5f3e7f6c`
  and registry `0095d4cd76ad5fdaeefeccdbb4322187892cc155bfac619ca4c8618ea50b9b20`.
- Stage 07 matched sizes: Fly 68,760; dense H=98/68,530; GRU H=43/68,853.
- DEC-027 and the approved Stage 01 experiment protocol.

## Execution contract

- Core order: fly-like, degree-preserving rewired, random sparse, GRU; dense last.
- Core runs use `200 + resume + 200` optimizer steps; dense uses `10 + resume + 10`.
- Batch 8, context 256, stride 128, four CPU threads, float32, AdamW with
  `lr=5e-4`, `weight_decay=1e-4`, no scheduler.
- Masking is temporal/channel/dropout `0.4/0.2/0.1`.
- Base seed 7; topology seed 7; topology-control seed 5007. Existing seed
  namespaces determine model, sample, temporal, channel and dropout streams.
- Full pretrain-domain validation occurs after each segment. `best.pt` is the
  earliest lowest exact record-to-domain macro `L_select`; only it is evaluated.
- Every process records one wall/steady-step/peak-RSS measurement. Stage 09 cost
  scenarios extrapolate 400, 2,000 and 50,000 steps across five seeds without
  selecting a future budget.

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| Pilot configs and deterministic manifest | `configs/pilot/stage08/` | Implementation |
| Minimal runner/report tooling and tests | `tools/`, `tests/` | Implementation |
| Ignored raw runs and checkpoints | `outputs/stage08-pilot/` | Director / Implementation |
| Tracked pilot summary | `reports/PILOT_RESULTS.{json,md}` | Director / Implementation |
| Stage records and notebook | `docs/research/stages/stage-08/`, `docs/research/` | Director |
| Independent verification | `docs/research/stages/stage-08/QA_REPORT.md` | QA |

## Acceptance criteria

- [x] M0 records PR #13 merged at `34b83c2` without altering Stage 07 evidence or QA.
- [x] Canonical validation aggregates valid targets to manifest records, dataset
  domains and equal-domain `L_select`; the earliest minimum selects `best.pt`.
- [x] All core arms match parameter tolerance, steps, samples, masking, optimizer,
  data order and CPU conditions; dense remains diagnostic-only.
- [x] Every core arm passes a common `1 + resume + 1` preflight before pilot launch.
- [x] Every real run preserves and hashes its pre-resume checkpoint and completes
  the approved split execution with finite values.
- [x] Bike-only evaluation derives seen channel counts only from pretrain domains;
  test/final-held-out requests hard fail and Electricity arrays remain unopened.
- [x] Exact config/source/manifest/registry/checkpoint/fixture hashes and runtime
  facts reproduce a byte-stable machine-readable and Markdown report.
- [x] Reports contain no winner, mean/significance claim, robustness pass/fail or
  prohibited Stage 08 interpretation.
- [x] Focused/full tests and governance/notebook validators pass; independent QA
  issues `PASS`, `CONDITIONAL PASS` or `FAIL`.

## User checkpoints

| Decision gate | When to ask | Current approval |
|---|---|---|
| Charter and implementation | Before tracked changes | `GO`, 2026-09-27 |
| Material scope/metric/data/budget change | Before affected work | `HOLD` if encountered |
| Pilot run | After all core preflights pass | `GO`, 2026-09-27; schema-v2 preflight passed |
| Result | After independent QA | `GO`, 2026-09-28 |
| Draft PR | After result `GO` | `GO`, 2026-09-28 |
| Merge | After Draft PR CI | pending separately |
| Stage 09 | Under a separately frozen charter | pending separately |

## Agent plan

- Research Director owns the stage, evidence integration and user gates.
- Experiment Scientist independently reviews execution fairness and report limits.
- Implementation Engineer is the sole tracked implementation/config writer.
- QA Engineer independently reruns checks without modifying tracked files.
- Data Scientist is not active; a corpus/role/split problem requires `HOLD` and a
  user-approved specialist substitution or budget expansion.

## Budget

```yaml
agent_budget:
  max_specialists: 3
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 1
  max_agent_report_words: 700
  user_approval_for_expansion: true
```

DEC-028 grants one bounded extra follow-up to the existing Implementation Engineer
and one bounded independent re-review to the existing QA Engineer. It does not add
a specialist or authorize the pilot run.

DEC-029 grants those same existing agents one further bounded remediation and
re-review for the two DEC-028 QA blockers. It does not authorize a schema-v2
preflight or pilot run.

DEC-030 grants one final bounded follow-up and re-review to replace the remaining
Git-history-dependent archival test. It does not authorize any public execution.

DEC-031 authorizes one new common schema-v2 `1 + resume + 1` preflight for all four
core arms in the fixed order. It does not authorize dense or the real pilot.

DEC-032 authorizes the fixed-order real pilot: 400 steps per core arm and the
20-step dense diagnostic. It does not authorize any rerun, final-held-out access,
Stage 09, PR or merge.

DEC-035 records the PI result `GO` and closes the bounded Stage 08 research stage.
It does not authorize a Draft PR, merge, Stage 09 or final-held-out access.

DEC-036 authorizes committing the reviewed Stage 08 changes, pushing the focused
branch, opening a Draft PR and observing its CI. It does not authorize merge.

## Risks and stop conditions

- Immediate `HOLD` on OOM, non-finite values, split/purge error, parameter or
  exposure mismatch, provenance/checkpoint mismatch or final-held-out access.
- Preserve a failed instrumentation/code-defect run; allow one same-config/seed
  diagnostic rerun only. No arm-specific budget/model change is automatic.
- A common setting change requires a new protocol version, user approval and rerun
  of every affected arm. Do not add seeds, domains, metrics or thresholds after results.

## User approval

- Decision: `GO`
- Date: 2026-09-27
- Conditions: implement the supplied Stage 08 plan through common preflight only;
  obtain a separate PI pilot-run `GO` before the 400-step/20-step real pilot.

## Result approval

- Decision: `GO`
- Date: 2026-09-28
- Scope: accept the bounded operational evidence and independent QA `PASS`; close
  Stage 08 without expanding any scientific claim.
- Boundary: Draft PR creation, merge, Stage 09 and final-held-out access require
  separate authorization.

## Integration approval

- Decision: `GO` for option A
- Date: 2026-09-28
- Scope: commit and push the Stage 08 branch, create a Draft PR and verify CI.
- Boundary: merge, Stage 09 and final-held-out access remain unauthorized.
