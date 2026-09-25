# Stage 04 Charter — Topology modularization

Status: closed

## Research question

Can the existing fly-like graph be extracted into a reusable topology artifact and builder while preserving graph, model, checkpoint, training, and evaluator behavior?

## In scope

- Extract only the current fly-like builder into `src/flyts/topology/` with validated graph artifacts and descriptive statistics.
- Route Foundation graph construction directly through the topology package; retain the legacy mask wrapper.
- Add a `fly_like` topology config default and preserve format-v1 strict loading and resume.
- Record pre-refactor CPU compatibility evidence and focused regression tests.

## Out of scope

- New topology generators, comparisons, performance claims, data/split/metric changes, threshold freeze, CUDA claims, and Stage 05 work.

## Inputs

- Base `origin/main` commit `f3362b24`; Stage 03 PR #9 is stale because its commits are already in main.
- Approved Stage 04 architecture contract supplied by Research Director; `docs/DEVELOPMENT_PLAN.md` Stage 04 and `docs/ARCHITECTURE.md`.

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| Builder, artifact, validation, statistics | `src/flyts/topology/` | Implementation |
| Compatible model/config/checkpoint path | `src/flyts/{model,foundation,training}.py` | Implementation |
| Golden graph and behavioral tests | `tests/test_topology.py` | Implementation |
| Interface and limitations | `docs/TOPOLOGY.md` | Implementation |
| Independent verification | Stage 04 QA report after handoff | QA |

## Acceptance criteria

- [x] Exact legacy graph edges over registered seeds, sizes and hub settings; validated artifact and documented graph statistics.
- [x] Existing state keys, tensor shapes, parameter registration order/count, and same-backend CPU outputs, gradients and training losses remain bitwise.
- [x] Legacy format-v1 checkpoints load strictly and resume with missing topology config canonicalized to `fly_like`.
- [x] Dense/scatter tolerance remains unchanged; runtime legacy checkpoint, training/resume and stable evaluator outputs are covered.
- [x] Focused and full tests, notebook/governance validators, and diff check pass; independent QA reports `PASS`.

## User checkpoints

| Decision gate | When to ask | Current approval |
|---|---|---|
| Stage charter/design | Before implementation | GO, 2026-09-25 |
| Material change to scope or contract | Before affected work | HOLD if encountered |
| Result/merge/Stage 05 | After independent QA | Result GO, 2026-09-25; merge and Stage 05 pending |

## Agent plan

- Primary owner: Research Director; one tracked-file implementation writer.
- Required specialists: none for implementation; independent QA after handoff.
- Why delegation is justified: independent verification of compatibility evidence.

## Budget

Single implementation owner; no subagents spawned by implementation. Stage result gate remains with the user.

## Risks and stop conditions

- Stop with HOLD on any changed golden edge, state key/parameter order, irreconcilable same-backend bitwise difference, required non-strict v1 load or format bump, or new scope choice.

## User approval

- Decision: GO
- Date: 2026-09-25
- Conditions: exact contract above; no new topology or scientific claim.
- Result decision: GO on 2026-09-25 after independent QA `PASS`; Draft PR requested. Merge and Stage 05 remain separately gated.
