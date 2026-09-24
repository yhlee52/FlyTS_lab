# Stage 01 Charter — Research and Experiment Protocol

Status: closed

## Research question

Can every planned FlyTS claim in Stages 2–10 be mapped, before further model changes, to a leakage-resistant and independently auditable protocol with fixed split roles, model selection, matched budgets, foundation metrics, and interpretable negative-result decisions?

## In scope

- formalize the FlyTS research question, H-01–H-04, and their claim boundaries;
- define development and final held-out domain roles and train/validation/test use;
- define seed/repetition, parameter matching, compute matching, and efficiency measurement;
- define masked reconstruction, channel permutation, channel dropout, unseen channel-count, frozen-probe, and held-out transfer evaluation;
- define support, no-support, harm, revisit, and stop rules;
- separate topology effects from tokenizer, router, and backbone effects;
- update consensus, protocol, traceability, decisions, risks, development status, and the shared notebook.

## Out of scope

- model, architecture, masking, router, backbone, or topology implementation;
- configuration, dataset, manifest, preprocessing, or training-behavior changes;
- downloading, converting, or admitting a new dataset;
- pretraining, performance comparisons, CUDA claims, or semiconductor work;
- Stage 02 implementation;
- numerical performance thresholds before Stage 03 evaluator calibration.

## Inputs

- `main` commit `ad9655f76bd140776514a4029ccc77ccf779b20f`;
- `docs/research/stages/stage-00/RESULT.md` and `QA_REPORT.md`;
- `docs/DEVELOPMENT_PLAN.md` Stage 1;
- `docs/VALIDATION.md`;
- current hypothesis, traceability, decision, risk, activation, and token-budget records;
- user-approved Stage 01 decisions dated 2026-09-24.

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| stage charter | `docs/research/stages/stage-01/CHARTER.md` | Research Director |
| project consensus | `docs/PROJECT_CONSENSUS.md` | Research Director; Program Integrator review |
| experiment protocol | `docs/EXPERIMENT_PROTOCOL.md` | Research Director; Experiment Scientist review |
| independent QA report | `docs/research/stages/stage-01/QA_REPORT.md` | Research Director records QA verdict |
| stage result | `docs/research/stages/stage-01/RESULT.md` | Research Director |
| aligned research records | `docs/research/` registers and notebook | Research Director |

## Acceptance criteria

- [x] The approved protocol covers all fourteen Stage 01 decision areas or explicitly assigns numerical calibration to Stage 03.
- [x] H-01–H-04 and R-01–R-08 map to a split, metric, aggregation, seed policy, budget rule, evidence stage, and claim boundary where applicable.
- [x] Train, validation, development held-out, final held-out, and test roles prevent target and selection leakage.
- [x] Domain-macro masked Huber selection, 1/3/5 repetitions, parameter tolerance ±5%, and optimizer-step matching are unambiguous.
- [x] Foundation metrics define direction, aggregation, paired controls, and the point at which numerical thresholds are frozen.
- [x] Topology, tokenizer, router, and backbone effects can be tested as single factors under matched conditions.
- [x] Negative and null outcomes map to support, no-support, harm, revisit, or stop without overstating claims.
- [x] No code, configuration, data, manifest, model behavior, training run, or performance claim changes.
- [x] Independent QA reports `PASS` or a fully resolved `CONDITIONAL PASS`.
- [x] The shared notebook and research-governance validator pass.

## User checkpoints

| Decision gate | When to ask | Current approval |
|---|---|---|
| Stage 01 charter and decision bundle | before tracked edits or specialist activation | approved (`GO`, 2026-09-24) |
| research question, split, metric, threshold timing, budget, scope, or acceptance change | before affected work continues | pending as needed |
| Architecture Scientist and specialist-budget expansion | before activation | pending as needed |
| Stage 01 result | before PR merge or Stage 02 | approved (`GO`, 2026-09-24); PR merge authorized, Stage 02 not authorized |

## Agent plan

- Primary owner: Research Director, the only tracked-document editor.
- Program Integrator: independently audit requirements, scope, traceability, and document consistency.
- Experiment Scientist: independently design and audit the split, metric, budget, evaluation, and negative-result protocol.
- Independent QA: verify leakage controls, selection/test separation, fairness, factor isolation, negative-result interpretation, unresolved decisions, and Stage 2–10 consistency.
- Conditional role: Architecture Scientist only after user approval if factor isolation cannot be specified within the approved team.
- Why delegation is justified: protocol design and requirements integration require distinct evidence, followed by independent acceptance.

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

- Stop before exposing final held-out domains or test results prior to the Stage 09 formal evaluation.
- Stop for user direction before changing any approved research question, split, metric, threshold timing, budget, scope, or acceptance criterion.
- Stop if a proposed comparison changes more than one of topology, tokenizer, router, or backbone.
- Do not convert Stage 03 calibration placeholders into numerical pass/fail thresholds in Stage 01.
- Do not force cross-domain probes when label ontologies are incompatible.
- Mark FLOPs as estimated or unverified when sparse/recurrent accounting is not reliable; optimizer steps remain the primary compute match.
- Stop before adding Architecture Scientist or exceeding the approved specialist/debate/follow-up budget.
- Do not interpret this documentation stage as evidence for foundation quality, transfer, topology benefit, or CUDA support.

## User approval

- Decision: GO
- Date: 2026-09-24
- Conditions: Execute only the approved documentation and protocol scope. Do not change model code, configuration, data, training behavior, research question, split, metrics, threshold timing, budget, scope, or acceptance criteria. Open a Draft PR, do not merge it, and do not begin Stage 02 without a separate user decision.
- Result gate: GO (`PASS` accepted, 2026-09-24). Close Stage 01 and merge PR #7; do not begin Stage 02 without a separate Charter approval.
