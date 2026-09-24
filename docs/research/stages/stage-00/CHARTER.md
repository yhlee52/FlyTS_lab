# Stage 00 Charter — Baseline Reproduction

Status: closed

## Research question

Can the merged foundation MVP be reproduced from a clean environment sufficiently to serve as the baseline for later FlyTS experiments?

## In scope

- install the project and development dependencies;
- run the full test suite;
- generate the synthetic corpus and run CPU smoke pretraining;
- verify checkpoint save/resume and embedding export;
- record environment, parameter count, timing, hashes, and failures;
- run CUDA checks only if suitable hardware is available.

## Out of scope

- architecture changes;
- new datasets or long pretraining;
- channel masking or topology baselines;
- performance or foundation-model claims.

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| baseline validation report | `docs/BASELINE_VALIDATION.md` | Implementation |
| ignored run artifacts | `outputs/phase0-baseline/` | Implementation |
| QA report | `docs/research/stages/stage-00/QA_REPORT.md` | QA |
| stage result | `docs/research/stages/stage-00/RESULT.md` | Research Director |

## Acceptance criteria

- [x] Project installation steps are recorded and reproducible.
- [x] Relevant tests pass, or each failure has a reproducible diagnosis.
- [x] CPU synthetic smoke pretraining completes with finite loss.
- [x] Checkpoint resume and embedding export complete.
- [x] CUDA status is measured or explicitly marked unavailable.
- [x] No existing validation claim is silently strengthened.
- [x] Shared notebook passes its validator.

## User checkpoints

| Decision gate | When to ask | Current approval |
|---|---|---|
| Stage 00 charter | before environment setup or implementation | approved (`GO`, 2026-09-24) |
| system-level install or paid compute | before action | pending as needed |
| scope, baseline protocol, or acceptance change | before affected work continues | pending as needed |
| Stage 00 result | before merge or Stage 01 | approved (`GO`, 2026-09-24) |

## Agent plan

- Primary owner: Implementation Engineer
- Required specialists: none by default
- Independent QA: QA Engineer
- Program Integrator: verify report paths and stage scope
- Delegation justification: separate implementation evidence from independent acceptance

## Budget

```yaml
agent_budget:
  default_mode: single_agent
  max_specialists: 2
  max_parallel_agents: 1
  max_debate_rounds: 0
  max_followups_per_agent: 1
  max_agent_report_words: 600
  user_approval_for_expansion: true
```

## Risks and stop conditions

- Stop for user direction before installing system-level software or using paid external compute.
- Do not treat missing CUDA hardware as a model defect.
- Stop and diagnose if repository behavior differs from the merged validation record.

## User approval

- Decision: GO
- Date: 2026-09-24
- Conditions: Execute the approved charter and checkpoint plan without changing architecture, datasets, model behavior, evaluation criteria, scope, or acceptance criteria. Hold before system-level installation, paid compute, or any material ambiguity or scope change. Keep implementation and independent QA separate, open a Draft PR, and do not merge it.
- Result gate: GO
- Result date: 2026-09-24
- Result conditions: Close Stage 00 and merge PR #6. Do not begin Stage 01 without separate approval of its charter.
