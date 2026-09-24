# Stage 02 Charter — Channel masking and dropout

Status: review
Date: 2026-09-24
Base commit: `8addce5`
Branch: `codex/stage-02-channel-masking`

## Research question

Can the existing channel-agnostic encoder train with full-channel reconstruction masking and input-only channel dropout while preserving visible-only statistics, exact legacy temporal masking, and version-1 checkpoint compatibility?

## Inputs and decisions

- Stage 01 approved protocol and result, `docs/PROJECT_CONSENSUS.md`, `docs/EXPERIMENT_PROTOCOL.md`, and `docs/DEVELOPMENT_PLAN.md` Stage 2.
- Approved Stage 02 architecture contract: dropout is input-only and sampled first; channel targets own temporal overlap; cause masks remain distinct; channel counts use seeded stochastic rounding; a visible observed sample is reserved.
- Fully hidden channels use pooled record-visible normalization. Validation uses temporal and channel targets without dropout. `C=1` channel masking and dropout are no-ops.

## In scope

- Independent masking module and configuration validation.
- Encoder and training integration with separate temporal, channel, dropout, visible, observed, missing, and padding masks.
- Focused leakage, invalid-mask, missing/padding, sampling, compatibility, and CPU resume tests.
- Small synthetic CPU smoke, documentation, and independent QA.

## Out of scope

- Stage 03 evaluator and thresholds; performance, foundation quality, topology, or CUDA claims.
- Architecture, tokenizer, router, backbone, model parameters, dataset eligibility or splits, metrics, or checkpoint format changes.
- Long training, company data, and final-test access.

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| Masking and integration | `src/flyts/masking.py`, `foundation.py`, `training.py`, `corpus.py` | Implementation Engineer |
| Configuration and tests | `configs/stage02_smoke.json`, `tests/test_masking.py` | Implementation Engineer |
| Behavior contract | `docs/MASKING.md` | Implementation Engineer |
| Stage and notebook records | `docs/research/stages/stage-02/`, `CURRENT_STATE.md` | Research Director / Implementation Engineer |
| Independent report | `docs/research/stages/stage-02/QA_REPORT.md` | QA Engineer |

## Acceptance criteria

- [x] Same seed reproduces masks; different valid seed changes sampled masks; low channel ratios can round to zero.
- [x] Original temporal-only masks and seed algorithm remain exact; version-1 checkpoints load and legacy/nested equivalent config resumes.
- [x] Config rejects both forms, missing forms, invalid ratios, and incompatible resume; old config files remain unchanged.
- [x] `C=1` channel mask/dropout are no-ops; channel-only batches with no target receive a precise error; 50% dropout forwards.
- [x] Full-channel target/dropout causes, overlap ownership, visible guard, missing/padding exclusion, and partial patches are verified.
- [x] Hidden and dropped perturbations do not affect visible representation or statistics; fully hidden targets use pooled record-visible normalization.
- [x] Paired mask permutation behavior and finite CPU forward/backward hold; unavailable CUDA is explicitly skipped.
- [x] Full tests, small synthetic CPU smoke and bitwise epoch-boundary resume, notebook/governance validators, and diff check pass.
- [x] Independent QA reports `PASS`; the result gate remains with the user.

## User checkpoints

| Gate | Current decision |
|---|---|
| Stage 02 charter and architecture contract | `GO`, 2026-09-24 |
| Protected research, architecture, data, metric, or budget change | `HOLD` until user decision |
| Stage 02 result / PR merge / Stage 03 | pending |

## Agent plan

One tracked-file implementation owner; independent QA reviews and writes only permitted temporary artifacts. The Research Director coordinates and records the human gate. Specialists do not spawn subagents.

## Budget

```yaml
agent_budget:
  default_mode: single_agent
  max_specialists: 3
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 1
  max_agent_report_words: 700
  user_approval_for_expansion: true
```

## Risks and stop conditions

- Fully hidden channels remain indistinguishable without identities or metadata.
- Channel-only masking can yield no targets, especially for a single-channel batch; training raises a clear error and recommends a positive temporal ratio.
- Stop for a protected decision change, long compute, or a checkpoint-format change. CUDA remains hardware-dependent and unverified.

## QA scope and remaining unverified

QA independently checks stochastic rounding, API guards, padding/missing masks, leakage, compatibility, resume, tests, and governance. A passing Stage 02 implementation does not establish robustness degradation, representation quality, topology benefit, CUDA support, or final-test performance.

## User approval

Decision: `GO`, 2026-09-24, for this bounded Stage 02 contract and acceptance criteria. The result decision remains pending.
