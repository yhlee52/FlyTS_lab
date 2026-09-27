# FlyTS Decision Log

## DEC-036 — Stage 08 Draft PR option A GO

- Date: 2026-09-28
- Decision authority: user selected option A and explicitly approved it.
- Decision: commit the reviewed Stage 08 changes, push the focused branch, create a
  Draft PR and observe its CI before returning to the user.
- Boundary: this decision does not authorize merge, Stage 09, pilot reruns,
  final-held-out access or any broader scientific claim.

## DEC-035 — Stage 08 result GO and closure

- Date: 2026-09-28
- Decision authority: user explicitly issued `GO` at the Stage 08 PI result gate.
- Decision: accept the bounded operational pilot evidence and independent QA
  `PASS`, and close Stage 08 without changing its protocol or claim scope.
- Evidence: all acceptance criteria are satisfied; the fixed single pilot completed,
  strict reports replay byte-for-byte, tests and validators pass, and independent
  post-pilot QA found no blocker.
- Boundary: topology/backbone superiority, robustness pass/fail, foundation quality,
  CUDA, transfer and semiconductor claims remain unverified. This decision does not
  authorize a Draft PR, merge, Stage 09 or final-held-out access.

## DEC-034 — Stage 08 independent post-pilot QA PASS

- Date: 2026-09-27
- Decision authority: independent QA Engineer under the approved Stage 08 plan.
- Decision: accept the completed evidence package for presentation at the PI result
  gate with QA status `PASS` and no blocker.
- Evidence: all 15 checkpoint/snapshot hashes and fixed execution facts match;
  histories are finite; earliest pretrain-only selection, Bike-only scope, exact
  provenance replay, focused/full tests, compilation and Git hygiene pass.
- Boundary: QA did not rerun the pilot, inspect Electricity arrays or validate CUDA.
  Resource values remain single-run CPU observations. Stage 09, PR and merge remain
  separately unauthorized.

## DEC-033 — Stage 08 fixed pilot evidence recorded

- Date: 2026-09-27
- Decision authority: execution under the user's DEC-032 pilot `GO`; no new
  research choice was made after observing results.
- Decision: accept the single completed fixed-order run as the sole Stage 08 pilot
  evidence pending independent QA. Generate and byte-check the tracked schema-v2
  reports without modifying the frozen protocol.
- Evidence: all four core arms completed 400 steps/3,200 samples; dense completed
  20 steps/160 samples; every run preserved its resume input and completed Bike-only
  evaluation. Full tests and required validators pass.
- Boundary: individual values and resource timings are descriptive only. No rerun,
  winner, threshold, Stage 09 budget, final-held-out access, PR or merge is approved.

## DEC-032 — Stage 08 real-pilot run GO

- Date: 2026-09-27
- Decision authority: user explicitly issued `GO` after reviewing the passing
  DEC-031 schema-v2 common-preflight evidence.
- Decision: run the four core arms in the frozen order for `200 + resume + 200`
  steps each, followed by the dense-leaky `10 + resume + 10` diagnostic, using
  the unchanged approved corpus, registry, configs, seeds and CPU environment.
- Boundary: no result-driven rerun, setting/metric/seed/domain change,
  final-held-out access, Stage 09, PR or merge is authorized. Results remain
  descriptive operational evidence and require independent QA and a PI result gate.

## DEC-031 — Stage 08 schema-v2 common-preflight GO

- Date: 2026-09-27
- Decision authority: user selected the recommended option after final DEC-030
  code QA `PASS`.
- Decision: run one new common schema-v2 `1 + resume + 1` preflight for the four
  core arms in the fixed order, using the unchanged approved corpus, registry,
  configs, seeds and CPU path. Preserve all earlier schema-v1 evidence.
- Boundary: no dense diagnostic, 400-step core pilot, result-driven rerun,
  final-held-out access, PR or merge is authorized. The real pilot still requires
  a separate PI `GO` after preflight evidence and independent verification.

## DEC-030 — Stage 08 history-independent archival-test exception

- Date: 2026-09-27
- Decision authority: user explicitly approved the final bounded exception after
  DEC-029 QA found one shallow-CI/offline compatibility blocker.
- Decision: permit the existing Implementation Engineer one final follow-up to
  replace `git show`-based Stage 07 archival validation with self-contained exact
  byte hashes, without changing the archived reports. Permit the existing QA
  Engineer one final independent re-review.
- Boundary: no research-setting or evidence change, new specialist, public
  preflight, pilot, final-held-out access, PR or merge is authorized.

## DEC-029 — Stage 08 execution-fact and archival-test remediation exception

- Date: 2026-09-27
- Decision authority: user explicitly approved a second bounded exception after
  the DEC-028 independent re-review remained `FAIL`.
- Decision: permit the existing Implementation Engineer one further follow-up to
  cross-check optimizer steps, exposure and parameter facts against bound evidence,
  and to make the Stage 07 test archival-aware without modifying frozen Stage 07
  evidence. Permit the existing QA Engineer one further independent re-review.
- Boundary: no specialist addition, research-setting change, schema-v2 preflight,
  pilot, final-held-out access, PR or merge is authorized. The preflight-evidence
  interpretation returns to the PI only after these two blockers pass.

## DEC-028 — Stage 08 QA-remediation budget exception

- Date: 2026-09-27
- Decision authority: user explicitly approved the requested bounded exception
  after the first independent Stage 08 QA verdict was `FAIL`.
- Decision: permit the existing Implementation Engineer one additional follow-up
  to bind all Stage 08 orchestration/config sources, strengthen report hash
  revalidation and separate setup, validation, checkpoint and evaluation cost
  evidence. Permit the existing QA Engineer one independent re-review.
- Boundary: no new specialist, data/arm/seed/metric/budget change, additional
  preflight rerun, 400-step/20-step pilot, final-held-out access, PR or merge is
  authorized. The separate pilot-run gate remains pending.

## DEC-027 — Stage 08 operational-pilot Charter GO

- Date: 2026-09-27
- Decision authority: user selected the recommended arm, step, evaluator,
  checkpoint, device, resume, training-profile, measurement and Stage 09 cost
  options, then explicitly requested implementation of the complete plan.
- Decision: run four matched core arms for one 400-step seed through a common
  multi-domain CPU path, with dense-leaky limited to a 20-step diagnostic. Use
  Stage 07 model sizes and runtime profile plus Stage 02 channel masking; select
  only `best.pt` by pretrain-domain `L_select`; split every run at its midpoint
  for resume; evaluate Bike descriptively; record single-pass wall/RSS evidence.
- Seeds and data: base/topology seed 7, topology-control seed 5007; Appliances and
  Beijing only for pretraining, Bike only for development evaluation, Electricity
  sealed. Stage 09 cost is scenario extrapolation, not a selected budget.
- Boundary: Charter GO authorizes M0-M4 implementation and common preflight. The
  400-step/20-step pilot requires a separate post-preflight PI `GO`. No final-held-out
  access, extra seed, threshold freeze, formal claim, merge or Stage 09 is authorized.

## DEC-026 — Stage 07 result GO

- Date: 2026-09-27
- Decision authority: user issued `GO` after reviewing the Stage 07 implementation, independent QA `PASS`, parameter-match evidence, cross-platform report remediation, and passing Draft PR #13 CI.
- Decision: accept and close the bounded conventional-backbone engineering stage. Fly sparse, dense-leaky and GRU now share the approved front end, routing, masking, reconstruction, evaluation and format-v1-compatible checkpoint paths; the frozen matched sizes and preregistered research roles are accepted as engineering evidence only.
- Evidence: `docs/research/stages/stage-07/{RESULT,QA_REPORT}.md`; Fly 68,760 parameters, dense-leaky `H=98`/68,530, GRU `H=43`/68,853, independent focused 64 passed/2 CUDA skips, full 97 passed/3 CUDA skips, deterministic reports, and both final Draft PR #13 CI jobs passed.
- Boundary: this does not authorize Draft PR #13 merge, Stage 08, real-data training, validation/final-held-out results, model selection, CUDA, transfer, foundation-quality, topology-benefit or backbone-superiority claims.

## DEC-025 — Stage 07 provenance-remediation budget exception

- Date: 2026-09-27
- Decision authority: user explicitly approved the requested bounded remediation after independent QA `FAIL`.
- Decision: increase only the existing Stage 07 Implementation Engineer's `max_followups_per_agent` from 1 to 2 to correct byte-level generated-config hashing, byte-oriented `--check`, complete report source binding and the focused provenance regression. The existing QA Engineer retains its original single follow-up for independent re-review.
- Boundary: no new specialist, model/config/matcher change, real-data run, performance evidence, Stage 08, PR merge or scientific claim is authorized.

## DEC-024 — Stage 07 conventional-backbone engineering GO

- Date: 2026-09-27
- Decision authority: user approved implementation of the complete Stage 07 plan and Charter after resolving the dense, GRU, parameter-budget, role, checkpoint, evidence, interface, initialization, staffing and compute options.
- Decision: retain the exact Fly sparse path; add a fully connected stabilized dense-leaky diagnostic and standard packed GRU formal candidate behind one shared routed-slot interface. Target 68,760 trainable parameters within plus or minus five percent, use synthetic engineering evidence only, preserve format-v1 checkpoints and preregister GRU/dense roles before performance.
- Initialization and evidence: preserve legacy Fly seeded behavior; copy allowlisted shared tensors from a deterministic Fly reference; isolate backbone/data/mask RNG; record actual parameters, schemas, finite gradients/update/resume and bounded analytic operation estimates without losses, rankings or runtime claims.
- Staffing: approve four specialists (Architecture, Experiment, one Implementation owner and independent QA), at most two parallel agents, one debate and one follow-up per specialist.
- Boundary: no real-data training, final-held-out/test access, Stage 08, threshold freeze, performance or scientific claim, merge or automatic advancement. Material deviation or budget expansion returns to `HOLD`.

## DEC-023 — Stage 06 result GO

- Date: 2026-09-27
- Decision authority: user issued `GO` after reviewing the Stage 06 evidence, independent QA `PASS`, and the fact that performance, foundation quality, transfer and final-held-out performance remain unverified.
- Decision: accept and close the bounded public-corpus v1 engineering stage. The official UCI Electricity 370-channel admission, fixed roles, chronological split/purge contract, hash-bound registry, complete source coverage and same-checkpoint finite smoke are accepted as engineering evidence only.
- Evidence: `docs/research/stages/stage-06/{RESULT,QA_REPORT}.md`; focused 8 passed, full 84 passed/3 CUDA skips, deterministic corpus report, full local source/array verification, and both Draft PR #12 CI jobs passed.
- Boundary: this does not authorize performance claims, final-held-out score access, Draft PR #12 merge, Stage 07, CUDA, transfer, foundation-quality or semiconductor claims.

## DEC-022 — Stage 06 public corpus v1 GO

- Date: 2026-09-27
- Decision authority: user approved implementation of the complete Stage 06 plan after selecting each material data, role, split, registry, validation, smoke and layout option.
- Decision: retain Appliances/Bike/Beijing; admit only official UCI ElectricityLoadDiagrams20112014 at native 370 channels/15 minutes; keep ETT and Traffic benchmark variants on `HOLD`. Separate dataset `domain_id` from semantic `domain_family`; assign Appliances/Beijing to `pretrain`, Bike to `development-held-out` and Electricity to `final-held-out`.
- Split and interface contract: chronological 70/15/15 per entity before windowing, 512-point validation/test purge, stable entity plus split-exclusive recording IDs, schema-v1 optional identity metadata, a manifest-hashed external role registry and legacy fallback. A dedicated streaming Electricity adapter preserves the existing CLI/API boundary.
- Validation and budget: convert and verify the full canonical corpus locally with fixture-only CI; use one frozen random-init format-v1 checkpoint for forward/encode-only shape/finite/memory smoke. Maximum three specialists, two parallel agents, one debate and one follow-up per agent.
- Boundary: no ETT/Traffic/321-derivative admission, pretraining, optimizer step, performance metric, final-held-out performance inspection, robustness freeze, scientific claim, merge or Stage 07. Material changes return to `HOLD`.

## DEC-021 — Stage 05 result GO

- Date: 2026-09-26
- Decision authority: user issued `GO` after reviewing the Stage 05 result, independent QA `PASS`, limitations, deterministic evidence, and Draft PR #11.
- Decision: accept the bounded topology-controls engineering result and close Stage 05.
- Evidence: `docs/research/stages/stage-05/{RESULT,QA_REPORT}.md`; focused 60 passed/two CUDA skips, full 76 passed/three CUDA skips, deterministic report check and validators passed, and Draft PR CI passed.
- Boundary: H-03, topology superiority, robustness, transfer, foundation quality, CUDA, biological mechanism, and semiconductor suitability remain unverified. This decision does not authorize merging PR #11 or beginning Stage 06; both require separate user direction.

## DEC-020 — Stage 05 extra QA follow-up approval

- Date: 2026-09-26
- Decision authority: user explicitly approved one additional independent QA verification after the first allowed remediation follow-up.
- Decision: permit the existing QA Engineer one extra bounded turn to rerun the final focused/full suites, report provenance check, governance/notebook validators, diff check, and Charter audit on the remediated commits.
- Boundary: this exception changes only `max_followups_per_agent` for this single Stage 05 QA re-review from 1 to 2. It does not add a specialist, change topology/seed/acceptance scope, authorize performance work, merge, or Stage 06.

## DEC-019 — Stage 05 overlap-guard revision GO

- Date: 2026-09-26
- Decision authority: user approved the Research Director's recommended revision after the preregistered fixed fixture entered `HOLD`.
- Evidence: the approved `N=64`, `E=613` fixture completed all `6,130` uniform valid swaps but retained `168/613 = 0.274062` reference edges; Implementation and Architecture found no straightforward correctness defect.
- Decision: retain uniformly proposed directed double-edge swaps, exact nodewise in/out degree and weak-component preservation, exactly `10E` accepted swaps and the `200E` attempt cap. Require a changed final edge set, but treat retained-edge fraction and Jaccard as descriptive statistics rather than pass/fail gates.
- Rationale: this preserves a conventional degree-matched null and avoids adding a result-optimizing proposal policy or choosing a post-hoc threshold just above the observed value.
- Boundary: all DEC-018 seed, provenance, CPU one-step, no-performance, agent-budget, merge, and Stage 06 restrictions remain unchanged.

## DEC-018 — Stage 05 topology controls GO

- Date: 2026-09-26
- Decision authority: user approved the full Stage 05 implementation plan and Charter.
- Decision: add exact directed in/out-degree-preserving rewiring and fixed-edge random sparse controls with matched N/E, annotations, parameters and model path; use `10E` accepted swaps, `200E` attempts, retained-edge fraction `<=0.10`, and at most 256 deterministic random candidates.
- Seed/provenance: retain `topology_seed`, add explicit `topology_control_seed`, derive kind-namespaced control seeds, preserve checkpoint format 1, and verify regenerated config graphs against stored buffers and provenance.
- Execution and staffing: synthetic CPU forward/backward/one-step only; Architecture, Implementation and independent QA specialists within the standard budget. No performance study or Experiment specialist.
- Boundary: no seed selection, mini-training, test/final-held-out access, Stage 06/07 work, topology/foundation/transfer/CUDA claim, merge, or Stage 06 start.
- Evidence target: `docs/research/stages/stage-05/CHARTER.md`; implementation, QA, result, and Draft PR follow within the approved stage.

## DEC-017 — Stage 04 result GO

- Date: 2026-09-25
- Decision authority: user accepted the Stage 04 result after independent QA `PASS` and requested a PR.
- Decision: close Stage 04 within its compatibility-only scope and prepare a Draft PR.
- Evidence: `docs/research/stages/stage-04/{RESULT,QA_REPORT}.md`; focused 13 passed, full 68 passed with three CUDA hardware skips, validators and diff check passed; Draft PR #10.
- Boundary: this does not authorize merge, Stage 05, a CUDA claim, topology comparisons or a topology-benefit claim.

## DEC-016 — Stage 04 topology modularization GO

- Date: 2026-09-25
- Decision authority: user approved the full Stage 04 design and acceptance contract.
- Decision: extract the exact fly-like graph into a reusable artifact, builder, validation and descriptive statistics interface. Foundation uses that interface directly; the legacy mask remains a wrapper. Preserve format-v1 strict checkpoint and same-backend CPU compatibility.
- Integration status: Stage 03 PR #9 is stale because its content is already in `origin/main` at `f3362b24`; Stage 04 starts from that main commit.
- Boundary: no random/rewired generator, topology performance claim, dataset or metric change, candidate-threshold freeze, or Stage 05 implementation.
- Evidence: `docs/research/stages/stage-04/CHARTER.md` and approved architecture contract.

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
