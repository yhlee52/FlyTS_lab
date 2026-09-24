# FlyTS Current Research State

Updated: 2026-09-24

## Current stage

Pre-stage 0 governance setup. `docs/DEVELOPMENT_PLAN.md` is merged; AI research-team governance is proposed in Draft PR #4.

## Current goal

Finalize a token-conscious, human-aligned Codex research team and its validation before Stage 0 begins, without changing model behavior.

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

## Open questions

- Whether the initial agent/model assignments need adjustment after real Stage 0 use.
- Whether a dedicated Research Ops agent is justified after pilot experiments begin.
- Exact hardware available for CUDA validation.

## Active risks

- The current environment used to inspect the repository lacks PyTorch and pytest.
- The foundation-model and topology-benefit claims remain unverified.
- Too many agents or full-lab reviews could waste tokens without improving evidence.

## Latest evidence

- Initial PoC and foundation MVP PRs are merged.
- Development plan PR #3 is merged.
- Draft PR #4 adds repository agent and skill configuration without model code changes.
- The user selected decision-gate checkpoints, mandatory clarification on ambiguity, and independent QA re-execution.
- The local research-governance validator passes for six specialist agents, two skills, the Stage 00 charter, and the shared notebook.

## Next action

Validate and review the human-aligned governance update, then request approval to merge the governance PR.
