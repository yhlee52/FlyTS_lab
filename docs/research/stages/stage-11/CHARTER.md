# Stage 11 Charter — Foundation Qualification Contract

Status: closed

PI requested implementation of this Stage 11 plan on 2026-10-11.

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
- Current `main` baseline: PR #19 merge commit
  `52fd44af0145e19d5f26138382bb0661e975eb09`, tree
  `618a9504ce6d10b2374f906613b3e91f2e0589f8`. Stage 10's PR #18 merge
  `a6000c14bce5fc655a2b7120acf09d430595e72b` is historical input.

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| Qualification contract and claim ladder | `docs/research/PHASE_02_FORMAL_VALIDATION_PLAN.md` | Research Director |
| Updated hypothesis and requirement-to-stage maps | `docs/research/HYPOTHESES.md`, `docs/research/REQUIREMENTS_TRACEABILITY.md` | Research Director; Program Integrator read-only review |
| Phase-specific risk additions | `docs/research/RISK_REGISTER.md` | Research Director |
| Stage 12–19 handoff and gate audit | `docs/research/stages/stage-11/RESULT.md` | Research Director; Program Integrator read-only review |
| Independent QA verdict | `docs/research/stages/stage-11/QA_REPORT.md` | QA Engineer; independent review |

## Acceptance criteria

- [x] The ultimate program objective and this phase's bounded objective are
  separate, falsifiable and consistent with DEC-070.
- [x] Q0–Q3 distinguish engineering operation, formal evaluation, bounded
  foundation-encoder evidence and connectome-specific evidence.
- [x] H-01–H-04 and R-01–R-08 map to named stages, evidence, controls and claim
  boundaries; R-09–R-12 retain their prospective gates.
- [x] A valid negative, inconclusive or infeasible result is an accepted outcome.
- [x] Dataset, protocol, compute, execution, final-unseal and publication gates
  remain separate and require the PI decisions stated in the phase plan.
- [x] Stage 12–19 scopes do not silently authorize data access or training.
- [x] Stage 09 artifacts and verdict remain byte/semantically immutable.
- [x] Notebook and governance validators pass; independent QA reports a verdict.

The PI authorized one additional bounded review (DEC-073). Independent QA
returned `PASS` on the corrected PR head `0effe407`; the PI accepted the Stage 11
result under DEC-074. Draft PR #20 remains unmerged.

## User checkpoints

| Decision gate | When to ask | Current approval |
|---|---|---|
| Phase objective | before drafting the stage plan | `GO`, Option A, 2026-09-30 |
| Stage 11 Charter | before Stage 11 implementation or specialist activation | `GO` for this document-only plan, 2026-10-11 |
| Qualification/claim change | before affected contract work continues | pending as needed |
| Stage 11 result | before Stage 12 Charter | `GO`, 2026-10-11 (DEC-074); Stage 12 data work still gated |

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

- Decision: `GO` for Stage 11 document-only contract work (DEC-072)
- Date: 2026-10-11
- Conditions: explicit PI request to implement the Stage 11 plan. Stage 11 result,
  Stage 12 Charter/data work and every later stage retain separate gates.
