# FlyTS Decision Log

## DEC-001 — Public data first

- Date: 2026-09-24
- Decision: Validate the generic representation model on public multivariate time-series data before semiconductor transfer.
- Evidence: project consensus and development plan
- Rejected alternative: semiconductor-specific first implementation
- Revisit when: FlyTS-Mini v0.1 stage gate is complete

## DEC-002 — Channel input is a set

- Date: 2026-09-24
- Decision: Do not bind the generic backbone to a fixed channel count or channel order.
- Evidence: target public domains and semiconductor recipe variability
- Rejected alternative: dataset-specific fixed channel projection
- Revisit when: metadata-aware identity is designed

## DEC-003 — Human stage gates

- Date: 2026-09-24
- Decision: The user approves stage scope, PR merge, and advancement.
- Evidence: requested advisor/customer operating model
- Rejected alternative: autonomous continuous stage advancement
- Revisit when: user explicitly changes governance

## DEC-004 — Concise shared notebook

- Date: 2026-09-24
- Decision: Agents share `CURRENT_STATE.md` and evidence links instead of full conversation transcripts.
- Evidence: token budget and context-quality requirements
- Rejected alternative: forwarding complete history to every agent
- Revisit when: a concrete handoff failure shows missing context

## DEC-005 — Selective agents

- Date: 2026-09-24
- Decision: Maintain a seven-role capability pool but activate only the smallest useful subset.
- Evidence: subagents duplicate model/tool work and coordination cost
- Rejected alternative: full-lab activation for every task
- Revisit when: stage retrospectives show insufficient independent review

## DEC-006 — Human alignment and ambiguity gate

- Date: 2026-09-24
- Decision: Stop and ask the user at material decision gates or whenever multiple plausible interpretations would change the work; agent consensus does not substitute for user intent.
- Evidence: explicit user request after reviewing the Agent/Skill/Harness design
- Operating rule: present options, recommendation, and impacts; treat no response as `HOLD`; record explicit "you decide" delegation
- Rejected alternative: agents resolving ambiguous requirements internally and reporting only the final conclusion
- Revisit when: the user explicitly changes the desired oversight level

## DEC-007 — Stage 01 research and experiment protocol

- Date: 2026-09-24
- Decision authority: user `GO` after reviewing the Stage 01 Charter and decision options
- User-selected rules: two-tier domain isolation; domain-macro masked Huber model selection; 1/3/5 smoke/development/formal repetitions; ±5% trainable-parameter tolerance; optimizer steps as the primary compute match; Stage 03 numerical-threshold calibration; separate interpolation and extrapolation channel-count evaluation; target-local frozen probes; one diagnostic rerun before final negative-result classification.
- Delegated and approved protocol details: final test first opens in Stage 09 after model/protocol freeze; record-to-domain macro aggregation with per-domain and micro diagnostics; cosine permutation distance with relative-L2 diagnostics; paired per-rate channel-dropout degradation; controlled time, memory, latency, parameter, and estimated-FLOPs reporting; single-factor isolation of topology, tokenizer, router, and backbone.
- Rejected alternatives: permanent single-domain holdout, full formal LODO at every stage, weighted composite selection, fixed three or five seeds at every stage, ±1% or component-exact parameter matching, FLOPs or wall time as the primary compute match, immediate numerical thresholds, extrapolation-only channel counts, mandatory source-trained probes, and zero or two diagnostic reruns.
- Impact: Stage 02 implements masking without performance gates; Stage 03 calibrates evaluator counts and numerical thresholds without final-test access; Stages 04–09 use the frozen protocol; Stage 10 packages already recorded final evidence.
- Revisit when: the user explicitly changes a protocol decision or Stage 03 calibration finds a metric technically invalid, in which case work returns to `HOLD` before revision.
- QA-blocker resolution approved by the user: unseen channel counts use paired relative domain-macro Huber degradation against the nearest seen-count nested view; target-local probes use macro-F1 for classification and train-standardized RMSE for regression against random-init and visible-statistics controls; H-03 uses paired domain-macro masked Huber against both rewired and random controls as its primary endpoint; masked Huber is fixed to Smooth L1 `beta=1.0` after train-only normalization. Stage 03 still owns numerical effect thresholds and uncertainty calibration, not these metric identities.

## DEC-008 — Stage 01 result gate

- Date: 2026-09-24
- Decision authority: user `GO` after reviewing the acceptance evidence, frozen protocol, independent QA `PASS`, limitations, and Draft PR #7
- Decision: close Stage 01 and authorize PR #7 for merge
- Boundary: this decision does not authorize Stage 02 implementation; Stage 02 requires its own Charter proposal and explicit user approval
- Evidence: `docs/research/stages/stage-01/RESULT.md`, `QA_REPORT.md`, and Draft PR #7

## DEC-009 — Stage 02 implementation contract

- Date: 2026-09-24
- Decision authority: user Stage 02 `GO` on the approved architecture contract and charter
- Decision: implement input-only channel dropout, full-channel reconstruction masking, separate causes with channel overlap ownership, visible-only statistics with pooled record fallback for fully hidden channels, and unchanged legacy temporal sampling and version-1 checkpoints.
- Boundary: no evaluator threshold, performance claim, model parameter, data split, or architecture direction change.
- Evidence: `docs/research/stages/stage-02/CHARTER.md` and `docs/MASKING.md`; QA and result gate pending.
