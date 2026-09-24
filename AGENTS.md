# FlyTS research instructions

## Mission

Build FlyTS as a channel-agnostic multivariate time-series foundation encoder. The first complete target is the public-data `FlyTS-Mini v0.1` evidence package defined in `docs/DEVELOPMENT_PLAN.md`; semiconductor transfer comes later.

## Start every material task

Read only what is needed, in this order:

1. `docs/research/CURRENT_STATE.md`
2. the active stage charter under `docs/research/stages/`
3. linked sections of `docs/DEVELOPMENT_PLAN.md`, architecture, dataset, or validation docs

Treat `CURRENT_STATE.md` as the shared lab notebook, not chat history. Update it with `$flyts-lab-notebook` after a material decision, experiment, PR, QA result, or handoff.

## Research-team operation

- Default to one primary agent. Use `$flyts-research-stage` only for a bounded research stage or stage review.
- The user is the academic PI/customer and final `GO`, `REVISE`, `HOLD`, or `STOP` authority.
- Only the Research Director may delegate. Subagents must not create subagents.
- Activate only roles justified by `docs/research/AGENT_ACTIVATION_MATRIX.md`.
- Follow `docs/research/TOKEN_BUDGET_POLICY.md`; do not run a full lab meeting for a routine edit.
- Give specialists a bounded context packet, not the full conversation.
- Keep the main thread focused on requirements, decisions, evidence, and user-facing outcomes.
- One implementation owner edits a code path at a time. Research and QA roles are read-only unless explicitly authorized.
- Preserve material dissent. Resolve unresolved scientific disagreement with a small experiment or user decision, not repeated debate.

## Research integrity

- Separate facts, inferences, hypotheses, and decisions.
- Mark unsupported claims `미검증`.
- Do not claim foundation-model quality, topology superiority, transfer, or GPU support without recorded evidence.
- Prevent target leakage and train/validation/test overlap.
- Keep topology comparisons matched on front-end, data, optimizer steps, and parameter/compute budget where feasible.
- Record dataset source, license/usage conditions, schema, split, and checksum.
- Keep company data, company checkpoints, sensitive metadata, raw data, and large artifacts out of public Git.

## Engineering workflow

- Work from the latest `main` on a focused branch.
- Preserve unrelated user changes.
- Use configuration-driven, modular CPU/CUDA-compatible code.
- Add or update tests for behavior changes.
- Run the smallest relevant checks first, then the broader suite required by the stage charter.
- Store committed source/config/docs in Git; keep `data/`, `outputs/`, checkpoints, arrays, and bundles ignored.
- Open a Draft PR with scope, evidence, limitations, and QA status. Do not merge without explicit user approval.

## Definition of done

A material stage task is not complete until:

- charter acceptance criteria are addressed;
- relevant tests or experiments have recorded provenance;
- independent QA has reported `PASS`, `CONDITIONAL PASS`, or `FAIL`;
- the shared lab notebook is current and validates;
- remaining risks and unverified claims are explicit;
- the user receives a concise stage-gate summary.

## Code review rules

Prioritize correctness, data/target leakage, split integrity, topology-comparison fairness, checkpoint compatibility, reproducibility, offline operation, and missing tests. Avoid style-only findings unless they hide a real defect.
