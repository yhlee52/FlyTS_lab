# Stage 11 Charter — Foundation Qualification Contract

Status: proposed

## Research question

Can FlyTS define a falsifiable, auditable qualification contract for evaluating
multichannel time-series foundation-model candidacy and connectome-specific value,
with explicit evidence levels and safe handoffs to data, protocol and execution
stages, before any new training begins?

## In scope

- Ratify the Phase 02 Q0–Q3 qualification and claim ladder.
- Map H-01–H-04 and R-01–R-08 to Stages 12–19 and their evidence owners.
- Define the minimum evidence categories that Stage 12 must make measurable.
- Define low/medium/high compute-envelope information required at Stage 13.
- Freeze stage ordering, user gates, QA responsibilities and stop conditions.
- Reconcile Stage 09 `HOLD` evidence with the new prospective phase without
  changing its reports, hashes or verdict.

## Out of scope

- Dataset download, admission, role or split changes.
- Architecture, tokenizer, router, topology or checkpoint-format changes.
- Metric thresholds, statistical rules, run matrix, seeds or compute approval.
- Training, evaluation, checkpoint creation, final-held-out access or publication.
- CUDA or semiconductor validation.

## Inputs

- `docs/research/PHASE_02_FORMAL_VALIDATION_PLAN.md`
- `docs/research/CURRENT_STATE.md`
- `docs/research/HYPOTHESES.md`
- `docs/research/REQUIREMENTS_TRACEABILITY.md`
- `docs/research/RISK_REGISTER.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- Stage 09 Charter, Readiness, Result and QA report
- Stage 10 Charter, Result and DEC-070 closeout decision
- GitHub `main` merge commit `a6000c14bce5fc655a2b7120acf09d430595e72b`,
  tree `8b39210d06a517b56f2aebbb35adf02b33259f71`

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| Qualification contract and claim ladder | `docs/research/PHASE_02_FORMAL_VALIDATION_PLAN.md` | Research Director |
| Updated requirement-to-stage map | `docs/research/REQUIREMENTS_TRACEABILITY.md` | Program Integrator |
| Phase-specific risk additions | `docs/research/RISK_REGISTER.md` | Research Director |
| Stage 12–19 handoff and gate audit | `docs/research/stages/stage-11/RESULT.md` | Program Integrator |
| Independent QA verdict | `docs/research/stages/stage-11/QA_REPORT.md` | QA Engineer |

## Acceptance criteria

- [ ] The ultimate program objective and this phase's bounded objective are
  separate, falsifiable and consistent with DEC-070.
- [ ] Q0–Q3 distinguish engineering operation, formal evaluation, bounded
  foundation-encoder evidence and connectome-specific evidence.
- [ ] H-01–H-04 map to named stages, evidence, controls and claim boundaries.
- [ ] A valid negative, inconclusive or infeasible result is an accepted outcome.
- [ ] Dataset, protocol, compute, execution, final-unseal and publication gates
  remain separate and require the PI decisions stated in the phase plan.
- [ ] Stage 12–19 scopes do not silently authorize data access or training.
- [ ] Stage 09 artifacts and verdict remain byte/semantically immutable.
- [ ] Notebook and governance validators pass; independent QA reports a verdict.

## User checkpoints

| Decision gate | When to ask | Current approval |
|---|---|---|
| Phase objective | before drafting the stage plan | `GO`, Option A, 2026-09-30 |
| Stage 11 Charter | before Stage 11 implementation or specialist activation | pending |
| Qualification/claim change | before affected contract work continues | pending as needed |
| Stage 11 result | before Stage 12 Charter or data work | pending |

## Agent plan

- Primary owner: Research Director.
- Required after Charter `GO`: Program Integrator for traceability and one
  independent QA Engineer for contract/gate review.
- Conditional: Experiment Scientist only if a statistical acceptance concept
  cannot be deferred cleanly to Stage 13.
- Implementation/Data/Architecture roles remain inactive; no code or data changes.
- Why delegation is justified: phase-level traceability and independent gate
  auditing materially reduce the risk of silently carrying Stage 09 assumptions.

## Budget

```yaml
agent_budget:
  default_mode: single_agent_until_charter_go
  max_specialists: 2
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 1
  max_agent_report_words: 700
  user_approval_for_expansion: true
```

## Risks and stop conditions

- `HOLD` if foundation-model qualification is defined as guaranteed success
  rather than a falsifiable evidence level.
- `HOLD` if exact dataset counts, statistical thresholds or compute are chosen in
  this stage without the Stage 12/13 evidence and PI gates.
- `HOLD` on any proposal to open Electricity, download/admit a target, start a
  run, create a checkpoint or modify Stage 09 evidence.
- Stop and ask the PI if Q2/Q3 meaning, H-04 necessity or the publication boundary
  admits materially different interpretations.

## User approval

- Decision: pending
- Date:
- Conditions: the Phase 02 objective is approved, but Stage 11 implementation,
  specialist activation and every later stage remain gated.
