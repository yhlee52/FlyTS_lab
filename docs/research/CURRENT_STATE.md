# FlyTS Current Research State

Updated: 2026-09-24

## Current stage

Stage 01 — Research and Experiment Protocol has completed document integration and independent QA `PASS` on `codex/stage-01-research-protocol` from `main` commit `ad9655f`. The stage is awaiting the human result gate.

## Current goal

Present the frozen research question, experiment protocol, traceability, independent QA evidence, limitations, and Draft PR for the Stage 01 result gate without beginning Stage 02.

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
- The user approved the Stage 00 result with `GO` on 2026-09-24 after QA `PASS`; this closes Stage 00 and authorizes PR #6 merge, but does not begin Stage 01.
- The user approved the Stage 01 Charter and decision bundle with `GO` on 2026-09-24. Stage 02 remains separately gated.
- Stage 01 uses two-tier domain isolation, domain-macro masked Huber selection, 1/3/5 repetitions, ±5% parameter tolerance, optimizer-step compute matching, and Stage 03 numerical-threshold calibration.
- Stage 01 also fixes interpolation/extrapolation channel-count evaluation, target-local frozen probes, one diagnostic rerun, and single-factor attribution for topology, tokenizer, router, and backbone.
- The user approved paired unseen/seen count degradation, task-specific controlled frozen probes, paired masked-Huber topology endpoints, and Smooth L1 `beta=1.0` to resolve the Stage 01 QA hold.

## Open questions

- Whether the initial agent/model assignments need adjustment after real Stage 0 use.
- Whether a dedicated Research Ops agent is justified after pilot experiments begin.
- When suitable CUDA hardware will be available for the still-unverified GPU path.

## Active risks

- Dependency minimums are not fully pinned, so a future fresh install may resolve versions different from this run.
- The current environment has a CPU-only PyTorch build and no CUDA device; GPU behavior remains unverified.
- The foundation-model and topology-benefit claims remain unverified.
- Too many agents or full-lab reviews could waste tokens without improving evidence.
- Premature final-test access, post-hoc threshold selection, or unmatched multi-factor comparisons could invalidate later claims.

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
- PR #6 contains only the five Stage 00 evidence and governance documents, and its GitHub Actions test workflow passed before the result gate.
- The Stage 01 branch was created only after local `HEAD`, `origin/main`, and fetched remote `main` matched at `ad9655f`.
- The Stage 01 Charter records the approved scope, acceptance criteria, decisions, agent budget, user gates, and stop conditions without changing code, data, configuration, or model behavior.
- Program Integrator and Experiment Scientist completed non-overlapping read-only reviews with no material disagreement or request to change an approved decision.
- `PROJECT_CONSENSUS.md` and `EXPERIMENT_PROTOCOL.md` now map the approved domain, selection, budget, evaluator, attribution, and negative-result rules into Stage 2–10 handoffs.
- H-01–H-04, R-01–R-08, DEC-007, RK-08–RK-12, and the development checklist are aligned to the Stage 01 protocol; all scientific hypotheses remain `미검증`.
- Independent QA issued `FAIL` because unseen channel-count and frozen-probe evaluations lack complete primary metric/control contracts, H-03 lacks a prespecified topology claim endpoint, and the Huber transition parameter is not fixed.
- The approved remediation now specifies all four missing contracts in DEC-007, project consensus, experiment protocol, hypotheses, and requirements traceability; scientific results remain `미검증` until later stages.
- Independent QA revalidated the approved remediation and issued final `PASS`; notebook, governance, and diff validation also pass.
- Draft PR #7 (`https://github.com/yhlee52/FlyTS_lab/pull/7`) is open from `codex/stage-01-research-protocol` at commit `e5aa72e`; it is unmerged and records the documentation-only scope, QA `PASS`, and remaining limitations.

## Next action

Present Draft PR #7 and request the user's `GO`, `REVISE`, `HOLD`, or `STOP` result-gate decision. Do not merge or begin Stage 02.
