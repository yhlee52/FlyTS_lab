# FlyTS Current Research State

Updated: 2026-09-24

## Current stage

Pre-stage 0 governance setup. `docs/DEVELOPMENT_PLAN.md` is merged; AI research-team governance is proposed in Draft PR #4.

## Current goal

Add a token-conscious Codex research team, concise shared lab notebook, stage-gate templates, and two repo-scoped skills without changing model behavior.

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
- `CURRENT_STATE.md` is the concise shared context, not a conversation transcript.
- Implementation and independent QA remain separate.

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

## Next action

Review and merge the research-team governance PR, then open Stage 0 with a bounded baseline-reproduction charter.
