# FlyTS Current Research State

Updated: 2026-09-24

## Current stage

Stage 00 — Baseline Reproduction has completed implementation and independent QA on `codex/stage-00-baseline-reproduction` from `main` commit `9a6f3d8`. The stage is awaiting the human result gate.

## Current goal

Present the recorded baseline evidence, independent QA result, limitations, and Draft PR for the user's Stage 00 gate without beginning Stage 01.

## Canonical references

- `docs/DEVELOPMENT_PLAN.md`
- `docs/ARCHITECTURE.md`
- `docs/DATASETS.md`
- `docs/VALIDATION.md`
- `docs/OFFLINE.md`
- `docs/research/TEAM_CHARTER.md`
- `docs/research/TOKEN_BUDGET_POLICY.md`

## Confirmed decisions

- The first complete target is public-data `FlyTS-Mini v0.1`.
- The user is the final stage-gate authority.
- The default workflow is single-agent; specialists are activated selectively.
- Only the Research Director delegates; recursive delegation is prohibited.
- The primary Codex agent is the Research Director; it directly delegates to specialist subagents.
- `CURRENT_STATE.md` is the concise shared context, not a conversation transcript.
- Implementation and independent QA remain separate.
- Material ambiguity is `HOLD`: ask the user with options, recommendation, and impacts before continuing.
- User confirmation is required for changes to research direction, architecture, data/splits, metrics/acceptance, scope, budget, or confirmed decisions.
- Explicit "you decide" delegation is itself a user decision and must be recorded.
- QA independently re-runs relevant checks and writes only temporary or Git-ignored artifacts.
- The user approved the Stage 00 charter and execution plan with `GO` on 2026-09-24.

## Open questions

- Whether the initial agent/model assignments need adjustment after real Stage 0 use.
- Whether a dedicated Research Ops agent is justified after pilot experiments begin.
- When suitable CUDA hardware will be available for the still-unverified GPU path.

## Active risks

- Dependency minimums are not fully pinned, so a future fresh install may resolve versions different from this run.
- The current environment has a CPU-only PyTorch build and no CUDA device; GPU behavior remains unverified.
- The foundation-model and topology-benefit claims remain unverified.
- Too many agents or full-lab reviews could waste tokens without improving evidence.

## Latest evidence

- Initial PoC and foundation MVP PRs are merged.
- Development plan PR #3 is merged.
- Research-team governance PR #4 and human-alignment PR #5 are merged in `main` commit `9a6f3d8`.
- The user selected decision-gate checkpoints, mandatory clarification on ambiguity, and independent QA re-execution.
- The local research-governance validator passes for six specialist agents, two skills, the Stage 00 charter, and the shared notebook.
- The Stage 00 branch was created only after local `HEAD`, `origin/main`, and fetched remote `main` were confirmed equal at `9a6f3d8`.
- The project-local Python 3.12 environment contains PyTorch 2.14.0+cpu and pytest 9.1.1; the full suite passed with 24 tests and one CUDA hardware skip.
- The CPU smoke run completed two finite-loss epochs with 17,936 parameters; epoch-boundary resume reproduced all 29 model tensors bitwise and embedding export produced finite `[9, 32]` vectors.
- Independent QA reproduced the corpus split and hash, exact smoke losses, bitwise resume, embedding schema, full tests, and CUDA-unavailable classification. After the notebook refresh and validator rerun, QA issued `PASS`.

## Next action

Open the Stage 00 Draft PR and request the user's `GO`, `REVISE`, `HOLD`, or `STOP` result-gate decision. Do not merge or begin Stage 01.
