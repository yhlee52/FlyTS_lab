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
- Evidence: `docs/research/stages/stage-02/CHARTER.md` and `docs/MASKING.md`; final QA and result authority are recorded separately in DEC-010.

## DEC-010 — Stage 02 result gate

- Date: 2026-09-25
- Decision authority: user `GO` after reviewing implementation evidence, compatibility, limitations, Draft PR #8, and final independent QA `PASS`
- Decision: accept the Stage 02 result and close the stage
- Delivery boundary: PR #8 remains unmerged for the user to merge directly
- Stage boundary: this decision does not authorize Stage 03; Stage 03 requires a separate Charter and explicit user approval
- Evidence: `docs/research/stages/stage-02/RESULT.md`, `QA_REPORT.md`, and PR #8

## DEC-011 — Stage 03 evaluator and calibration candidate GO

- Date: 2026-09-25
- Decision authority: user `GO` on the Stage 03 Charter and detailed implementation plan
- Decision: implement an offline robustness evaluator with a minimal `encode/reconstruct/provenance` adapter; fixed deterministic paired fixtures; Smooth L1 `beta=1.0`; record/domain-macro primary; permutation, dropout, count, padding and missingness checks.
- Calibration approval: synthetic controls plus exact-hash public development-only evidence; seeds `7/17/29`, 400 optimizer steps each, 95% paired hierarchical bootstrap with 10,000 resamples. Hard reject test/final-held-out access.
- Boundary: numerical guards, thresholds and uncertainty config are `candidate` only. User threshold decision is a mandatory HOLD. No stage closure, final QA or merge is authorized by this decision.
- Evidence: `docs/research/stages/stage-03/CHARTER.md`, `docs/EVALUATION.md`; candidate report follows only if the exact public corpus is available.

## DEC-012 — Stage 03 normalization clarification and one follow-up budget exception

- Date: 2026-09-25
- Decision authority: user explicitly selected option A and approved one additional Implementation Engineer follow-up.
- Decision: retain train-visible-only fitted preprocessing. Stage 03 paired scoring uses one nonparametric record-local reference coordinate derived only from the intersection of both views' visible non-target context; targets, corruption, dropout, missingness and padding never enter its statistics. The coordinate is recomputed per pair and is not a fitted preprocessing parameter.
- Execution: rebuild only the exact approved public starter corpus hash if canonical LF manifest serialization is required; run seeds `7/17/29` for 400 optimizer steps each and use `last.pt` for development calibration. Do not use `best.pt` as a protocol-compliant primary selection claim.
- Budget: the user approved one extra bounded implementation follow-up to resolve QA findings and produce candidate evidence; the other specialist limits remain unchanged.
- Boundary: all guards, thresholds and uncertainty results remain `candidate`; Stage 03 threshold decision is still `HOLD`.

## DEC-013 — Stage 03 candidate gate: GO to defer freeze

- Date: 2026-09-25
- Decision authority: user `GO — defer freeze` after reviewing candidate evidence and remediation QA `PASS`.
- Decision: accept the evaluator/calibration candidate evidence milestone for user review, while deferring threshold, numerical guard and uncertainty-config freeze. Their values remain `candidate`.
- Boundary: Stage 03 stays active/open. This decision does not authorize final Stage 03 QA, stage closure, a Draft PR, merge or Stage 04. Additional evidence scope requires separate user approval; until then the next action is `HOLD`.
- Evidence: `reports/robustness/calibration-candidate-v1.{json,csv,md}` and the Stage 03 Charter checkpoint.

## DEC-014 — Stage 03 closure path without numerical freeze

- Date: 2026-09-25
- Decision authority: user explicitly approved closing Stage 03 without freezing thresholds, numerical guards or uncertainty configuration and authorized a Draft PR after independent final QA.
- Decision: accept the evaluator and development-only calibration candidate evidence as a bounded engineering result. Numerical settings remain `candidate` and unfrozen; reported robustness metrics are descriptive only. No robustness pass/fail or final foundation-quality claim is allowed until a separately approved reopening and freeze.
- Evidence interpretation: sparse channel-count arms and absent executed sensitivity calibration make an effect-threshold freeze unsupported. This is an interpretable no-freeze outcome, not a negative model-quality claim.
- Boundary: Stage 03 is in closure review, not closed before independent final QA. Stage 04 and PR merge are not authorized by this decision.
- Evidence: `docs/research/stages/stage-03/CHARTER.md`, `RESULT.md` (draft), and `reports/robustness/calibration-candidate-v1.{json,csv,md}`.

## DEC-015 — Stage 03 no-freeze closure after final QA

- Date: 2026-09-25
- Decision authority: user-approved DEC-014 closure path; independent QA supplied the final gate verdict.
- Outcome: final independent QA reported `PASS — approved evaluator and candidate deliverables under no-frozen-threshold closure`. All eight Charter acceptance criteria are satisfied in that scope; Stage 03 is closed and the user-authorized Draft PR may be prepared.
- Boundary: thresholds, numerical guards and uncertainty configuration remain `candidate` and unfrozen; robustness metrics are descriptive only. Formal pass/fail requires separately approved reopened calibration and freeze. PR merge and Stage 04 require separate user approval.
- Evidence: `docs/research/stages/stage-03/QA_REPORT.md`, `RESULT.md`, and `reports/robustness/calibration-candidate-v1.{json,csv,md}`.
