---
name: flyts-research-stage
description: Run one bounded FlyTS research stage with selective AI-agent staffing, evidence-based lab review, independent QA, and a human stage gate. Use when starting, continuing, reviewing, or closing a numbered FlyTS stage; when the user asks the FlyTS research team to work; or when a lab meeting or stage decision is required. Do not use for a trivial one-file edit that does not change research state.
---

# Run a FlyTS Research Stage

Treat the repository as a research lab. Advance only one approved stage at a time and keep the user as the final decision-maker.

## Load the minimum state

Read in this order:

1. `AGENTS.md`
2. `docs/research/CURRENT_STATE.md`
3. The active stage charter under `docs/research/stages/`
4. Only the sections of `docs/DEVELOPMENT_PLAN.md` and other documents linked by the charter

Do not load old meeting transcripts or unrelated stage reports unless a concrete question requires them.

## Open the stage

Confirm the stage has one primary research question, explicit scope, measurable acceptance criteria, named deliverables, a delegation budget, and a user approval state. If the charter is missing, draft it from `docs/research/templates/STAGE_CHARTER.md` and stop for user approval before implementation.

## Staff selectively

Default to the primary agent working alone. Activate specialists only when role separation adds material value. Follow `docs/research/AGENT_ACTIVATION_MATRIX.md` and `docs/research/TOKEN_BUDGET_POLICY.md`. Only the Research Director may delegate. Do not allow recursive delegation.

Give each specialist only the assigned question, relevant paths, confirmed constraints, expected output and length, and an explicit stop condition. Ask for conclusions, evidence, risks, recommended action, and files examined. Do not request raw exploration logs in the main thread.

## Run the stage

1. Collect independent memos only when parallel evidence or disagreement is useful.
2. Allow at most one focused rebuttal round.
3. Record material decisions or dissent, not transcripts.
4. Let one implementation owner modify a code path at a time.
5. Run tests and experiments with provenance.
6. Obtain independent `PASS`, `CONDITIONAL PASS`, or `FAIL` from QA.
7. Update the notebook with `$flyts-lab-notebook`.
8. Present evidence, risks, QA status, artifacts, and a `GO`, `REVISE`, `HOLD`, or `STOP` request.

Do not merge, expand scope, or begin the next stage without explicit user approval.
