# FlyTS Phase 02 — Formal Training and Scientific Evaluation

Status: Stage 11 contract accepted by PI (DEC-074); independent QA `PASS`;
phase objective approved by the PI

Decision basis: DEC-071, 2026-09-30; Stage 11 Charter `GO` granted by the PI
on 2026-10-11. DEC-074 accepted the Stage 11 result; later stage gates remain
pending.

The Stage 01 `docs/EXPERIMENT_PROTOCOL.md` and the Stage 09 protocol-v2 60-run,
five-seed proposal record earlier rules and an unfrozen historical plan. Stage 09
closed at `HOLD` with final QA `FAIL`. Neither its numerical candidates nor its
matrix are a Phase 02 freeze. Historical Stage 09 and Stage 10 execution/release
language in `docs/DEVELOPMENT_PLAN.md` is read with those later decisions and
DEC-070, not as present execution or publication authority.

## Program objective

The long-term program objective is to determine, with reproducible public-data
evidence, whether FlyTS qualifies as a multichannel time-series foundation model
and whether its fly-connectome-inspired topology contributes value beyond the
channel-agnostic front-end and matched controls.

This is an evidence-seeking objective, not a presumption that the hypotheses are
true. A valid `no-support`, `harm`, `inconclusive` or infeasible result is a
scientifically complete outcome when produced under the frozen protocol.

## Phase objective

Using public data only, freeze data roles, evaluation rules and compute budgets
before viewing formal results; execute matched multi-seed experiments for H-01
through H-03; select at most one private checkpoint candidate using development
evidence only; and evaluate H-04 or final-held-out evidence only after its own
admission, readiness and PI gates.

No checkpoint, package or model release is part of this phase. DEC-070 remains in
force unless a future, separate PI decision explicitly changes it.

## Primary research questions

1. Does one FlyTS encoder retain useful representations across channel order and
   supported seen/unseen channel counts under a preregistered H-01 contract?
2. Does channel masking/dropout improve registered missing-sensor robustness
   without unacceptable clean-input or representation harm under H-02?
3. Does the fly-like recurrent topology outperform matched rewired and random
   sparse controls under H-03, with tokenizer, router, data, exposure and compute
   held fixed?
4. If an eligible labeled target is admitted, do frozen FlyTS representations
   improve target-local tasks over random-initialized and visible-statistics
   controls under H-04?

## Qualification and claim ladder

| Level | Evidence required | Permitted interpretation |
|---|---|---|
| Q0 — engineering MVP | Existing Stage 08/10 engineering evidence | The pipeline and checkpoint workflow operate in the recorded CPU environment. |
| Q1 — formally evaluated encoder | Frozen protocol, valid multi-seed execution, independent QA and bounded outcomes for H-01–H-03 | FlyTS has been formally evaluated on the named public domains and budgets. |
| Q2 — bounded foundation-encoder evidence | Q1 plus preregistered support for variable-channel behavior, robustness and reusable representations, including H-04 on admitted target tasks | Evidence supports foundation-encoder candidacy only within the tested domains, tasks, channel ranges and budgets. |
| Q3 — connectome-specific FlyTS evidence | Q2 plus H-03 support against both matched topology controls | The tested fly-like topology contributes under the frozen comparison; no universal topology claim follows. |

Q0 records bounded CPU engineering operation; it does not imply any H-01–H-04
support. Q1 requires valid, frozen, multi-seed H-01–H-03 outcomes and independent
QA, including valid negative outcomes; it means formally evaluated, not that every
hypothesis was supported. Q2 additionally requires preregistered positive evidence
for variable-channel behavior, robustness and H-04 reusable representations on an
admitted target. Q3 additionally requires H-03 support against *both* matched
rewired and random sparse controls. Failure of either contrast cannot be rescued
by a secondary endpoint. Q2 and Q3 thresholds, minimum domain/task coverage and
uncertainty rules require Stage 12 adequacy evidence and Stage 13 PI-approved
freeze before formal results. This phase cannot establish a universal
foundation-model, production, CUDA or semiconductor claim.

If H-01/H-02/H-04 support but H-03 does not, evidence may support the
channel-agnostic encoder but not a connectome-specific advantage. If H-04 cannot
be admitted, Q2/Q3 are not reached and H-04 remains `not tested`.

A valid `no-support`, `harm`, `inconclusive`, or infeasible result is a research
outcome, not a reason to alter a frozen design after viewing results. If an
unresolved integrity defect prevents valid formal inference, the phase can close
at `HOLD`/`STOP` with Q0 as its highest evidenced level and the untested
hypotheses explicit. No Q level is awarded from a proposed protocol, a failed
QA review, or a missing prerequisite.

## Stage 11 qualification-to-evidence contract

| Item | Evidence and control to register in later stages | Evidence owner and claim limit |
|---|---|---|
| H-01 / R-01 / R-02 | Stage 12 checks independent records, seen/unseen count coverage and valid paired nested views; Stage 13 freezes permutation/count endpoints and rules; Stage 14 rehearses paired masks and leakage guards; Stages 15–16 execute and analyze, with final evidence only after Stage 17. | Stage 12 Data, Stage 13 Experiment, Stage 14 Implementation/QA, Stages 15–16 Experiment, Stage 18 final QA. Count behavior and global representation invariance only within admitted domains and ranges. |
| H-02 / R-04 | Stage 12 checks missingness and usable paired corruption views; Stage 13 freezes dropout, clean-harm and uncertainty rules; Stage 14 checks target/reference separation; Stages 15–16 execute and analyze matched masking controls. | Stage 12 Data, Stage 13 Experiment, Stage 14 QA, Stages 15–16 Experiment. Registered missing-channel corruption only. |
| H-03 / R-05 | Stage 13 freezes two primary topology contrasts and single-factor matching; Stage 14 validates graph, front-end, steps, exposure and parameter tolerance; Stages 15–16 execute and analyze both matched controls. | Stage 13 Experiment, Stage 14 QA, Stages 15–16 Experiment. A null or harmful topology result does not refute front-end behavior. |
| H-04 | Stage 12 audits eligible labeled target, ontology, independent groups and split without opening target test; Stage 13 freezes general probe, control, effect and analysis rules; Stage 17 binds an approved target-specific packet before separate H-04/test access; Stage 18 runs once. | Stage 12 Data, Stage 13 Experiment, Stage 17 Data/Experiment/QA, Stage 18 Experiment/QA. Target-local transfer within admitted task families only; without admission it is `not tested`. |
| R-03 | Stage 12 checks signal-only schema, Stage 13 registers the metadata-absent path, Stage 14 verifies it against frozen manifests, and later runs record whether metadata was used. | Stage 12 Data, Stage 13 Experiment, Stage 14 Implementation/QA, Stages 15–16 Experiment. Optional metadata operation, not equal quality. |
| R-06 / R-07 | Stage 14 checks the exact device environment and closed-network preflight; Stage 15 records actual training-device evidence. | Stage 14 Implementation/QA and Stage 15 Experiment/QA. CPU evidence cannot establish CUDA; offline evidence binds only its tested bundle. |
| R-08 | Stage 19 records the public-data conclusion and a separate later PI gate. | Stage 19 Director/QA. No semiconductor suitability or adaptation claim in Phase 02. |

Stage 19 maps recorded valid evidence to Q0–Q3. Existing H/R statuses and Stage 09
findings remain historical; this table assigns prospective responsibility only.

## Required Stage 12 and Stage 13 handoffs

Stage 12 must measure, for each existing or proposed public domain, source rights
and checksums; schema, timestamp/sampling and missingness semantics; independent
record, entity/subject and time-range units; split-before-windowing and purge
feasibility; leakage and train-only preprocessing boundaries; seen/unseen channel
count distribution and paired interpolation/extrapolation views; and, for H-04,
target labels, class/task-family coverage, ontology compatibility, group-disjoint
splits and target-test sealing. It must state where evidence is insufficient and
prepare a separate PI decision for each source, role and split. Measurement does
not admit a dataset or change a role.

Stage 13 must present low, medium and high resource envelopes using Stage 12
evidence. Each option must state its candidate arm/run and seed structure,
optimizer steps and exposure, setup/data preparation, training, validation,
evaluation and checkpoint time, peak memory and disk, exact hardware/software
environment, estimator basis and uncertainty, failure/diagnostic allowance, and
which registered claims fit the envelope. FLOPs, wall time and steps must remain
distinct quantities. Stage 13 recommends one option for explicit PI approval and
freezes endpoints, numerical guards, uncertainty/multiplicity, selection and the
run matrix before any formal result; Stage 11 selects no values or option.

## Data and artifact boundary

- Current roles remain the starting point: Appliances and Beijing `pretrain`,
  Bike `development-only`, Electricity `final-held-out` and sealed.
- Stage 12 may propose new development or labeled target domains, but admission,
  role, split, license and schema each require an explicit PI gate.
- HAR and HARTH remain excluded unless their recorded blockers are resolved under
  a new admission decision; no silent substitution or split search is allowed.
- Every formal run records source/array manifests, split identity, Git commit,
  config hash, seed hierarchy, graph identity, environment and artifact hashes.
- Checkpoints, embeddings, raw data and run outputs stay in ignored local storage.
  They are never committed or publicly uploaded during this phase.

## Stage plan

| Stage | Purpose | Main deliverables | Exit gate |
|---:|---|---|---|
| 11 — Qualification contract | Turn the approved objective into falsifiable qualification levels, hypotheses, claim boundaries, stage ownership and required later compute-envelope fields. | Stage Charter, qualification matrix, updated traceability and risks, Stage 12/13 handoff requirements. | PI decides whether to accept the contract and authorize drafting a Stage 12 Charter. No dataset or budget approval. |
| 12 — Data and evaluation adequacy | Determine whether existing and candidate public domains provide enough independent records, channel-count coverage and eligible target tasks without leakage or rights ambiguity. | Dataset admission packets, role/split manifests, independent-unit audit, H-01/H-02 coverage analysis and H-04 target decision. | PI approves every new source/role/split; otherwise `HOLD` or reduce the registered claim set. |
| 13 — Protocol v3 and budget freeze | Freeze endpoints, guards, minimum effects, uncertainty/multiplicity rules, seeds, comparison arms, checkpoint selection, run matrix and compute budget before formal results. H-04 general rules are frozen here; Stage 17 may bind only a previously approved target-specific packet without changing them. | Hashed protocol v3, configs, run matrix, statistical analysis plan, low/medium/high estimates and freeze manifest. | Independent pre-freeze QA `PASS` plus explicit PI protocol/budget `GO`. Any material later change creates v4 before affected execution. |
| 14 — Execution preflight | Prove that the frozen runner, reporter, cache, checkpoint, resume and failure paths work end to end without using formal/final evidence. | Synthetic/tiny blind rehearsal, runtime/memory evidence, deterministic manifests, no-network test and preflight QA report. | QA `PASS`; predicted resources fit the approved envelope. CUDA use requires a separately validated exact environment. |
| 15 — Formal multi-seed training | Execute the frozen H-01–H-03 matrix without adaptive changes, result-driven stopping or added runs. | Local checkpoints, run manifests, logs, failure ledger, exact exposure/compute records and sealed evaluation inputs. | All planned runs are valid, or the preregistered failure/diagnostic rule yields `HOLD`/`STOP`. No final-held-out access. |
| 16 — Development evaluation and selection | Apply the frozen analysis plan, issue bounded H-01–H-03 outcomes and select at most one private checkpoint using development evidence only. | Locked report, sufficient statistics, hypothesis outcomes, selection ledger and checkpoint provenance. | Independent QA `PASS`; PI accepts the outcomes and either one candidate or an explicit no-candidate result. |
| 17 — Transfer/final readiness | If Stage 16 selected a candidate, audit one-time Electricity final orchestration. If Stage 12 separately admitted an H-04 target, also bind its target-specific packet to Stage 13 frozen rules. | Conditional target protocol binding, ontology/split evidence, final access ledger, unseal rehearsal and readiness QA. | Separate PI `GO` for H-04 execution and/or the one-time Electricity final open. Missing H-04 prerequisites keep H-04 `not tested`; without a candidate, skip final execution and record why. |
| 18 — One-time final evaluation | Evaluate the already selected checkpoint once on the frozen final/target evidence; never tune, rerank or add runs from the result. | Atomic unseal record, final predictions/sufficient statistics, locked report and independent QA. | PI accepts `support`, `no-support`, `harm`, `inconclusive` or invalid/stop outcome. No automatic rerun. |
| 19 — Phase closeout | Map all valid outcomes to Q0–Q3, decide private checkpoint retention and record limitations and the next research decision. | Final evidence matrix, model card update, private checkpoint disposition, phase result and QA report. | PI `GO`, `HOLD` or `STOP`. Publication remains a separate future decision and defaults to no release. |

### Proposed narrow engineering track after DEC-112

The PI selected route A in
`stages/stage-13/NARROW_PREFLIGHT_PROPOSAL.md`: prepare a CPU-only, synthetic
Stage 14 engineering preflight to reduce the cost of the stalled eligibility
search. The [Stage 14 Charter proposal](stages/stage-14/CHARTER.md) defines a
separate pre-execution QA, exact resource/run PI gate and bounded result QA.
The engineering Charter received PI `GO` in DEC-114 after an independent
`CONDITIONAL PASS` and a Director correction that was not independently
delta-reviewed. Its exact manifest, pre-execution QA and resource/run gate
remain pending; the formal Stage 13 and formal Stage 14 exit requirements in
the table remain unchanged.
Engineering-track completion permits only a bounded Q0 operational statement.
It cannot establish H-01–H-04 outcomes, Q1–Q3, formal Stage 14 completion or
Stage 15 entry. No real data, Electricity/test, CUDA, source admission or
release permission follows from DEC-112.

## Cross-stage invariants

- Stage 09 reports, hashes, `HOLD` and final QA `FAIL` remain historical and are
  never rewritten or presented as Phase 02 evidence.
- Formal results cannot select new domains, metrics, thresholds, seeds, arms or
  budgets. A material change requires a new protocol version and PI approval.
- Electricity and any target test split remain sealed until the Stage 17 gate.
- Model selection uses only the frozen development metric and policy. Final
  evidence cannot tune, filter, rerank or rescue a development result.
- All topology comparisons are single-factor and matched on the declared shared
  components, optimizer steps, exposure and parameter tolerance.
- Failed, interrupted and excluded runs remain in the ledger. Only a
  preregistered diagnostic rerun is allowed without a new protocol.
- Valid negative results complete the relevant stage; they do not authorize
  architecture searching after results are seen.

## Phase-level success criteria

The phase is complete when:

- Stages 11–16 produce a frozen, independently audited formal evidence package,
  or an explicit `HOLD`/`STOP` identifies why valid execution is infeasible;
- H-01–H-03 each receive a bounded valid outcome or an explicit `not tested`/
  invalid status with the `HOLD`/`STOP` cause rather than an implied positive claim;
- H-04 is either executed under an admitted target contract or remains clearly
  `not tested`;
- at most one development-selected private checkpoint is retained, or the record
  explicitly states that no checkpoint qualified;
- no final-held-out result affected training, thresholds or selection;
- the Q0–Q3 qualification level is assigned from recorded evidence; and
- independent QA and the PI accept the phase result.

Scientific success is valid evidence, not necessarily a positive model result.

## User gates

| Gate | Required before | Current state |
|---|---|---|
| Phase objective | Drafting this stage plan | `GO`, Option A, 2026-09-30 (DEC-071) |
| Phase stage plan and Stage 11 Charter | Beginning Stage 11 implementation | `GO` requested by PI on 2026-10-11 for Stage 11 document work only |
| Stage 11 result | Drafting a Stage 12 Charter | `GO`, 2026-10-11 (DEC-074); does not authorize data work |
| Stage 12 Charter and each dataset/role/split | Any Stage 12 data access or changed source/role/split | Charter `GO` DEC-075; bounded three-source access DEC-076/077 and source/use, role, split decisions DEC-078; Stage 12 result `GO` DEC-079. New sources/changes still require separate PI decisions. |
| Stage 13 Charter and candidate discovery/access | Stage 13 work beyond a proposal or any new-source search/read | Charter `GO` DEC-082; bounded metadata-only discovery `GO` DEC-083; PhysioNet sidecar inventory `GO` DEC-084 and six specified EDF headers `GO` DEC-085. Signal/archive access, admission, role and split remain separate PI decisions. |
| Protocol v3 and compute budget | Any formal training | pending Stage 13 result |
| Formal execution | Starting Stage 15 | pending preflight QA and explicit PI `GO` |
| H-04/final unseal | Any target-test or Electricity final access | pending Stage 17 and explicit PI `GO` |
| Phase result | Closing Stage 19 or starting another phase | pending |
| Public release | Tag, GitHub release, PyPI or checkpoint publication | prohibited by DEC-070; requires a separate future decision |

## Staffing and budget policy

- The Research Director owns phase alignment and every PI gate.
- Each stage receives its own Charter and minimal specialist set under the current
  activation matrix and token policy.
- Data admission, protocol freeze, formal interpretation and final opening use
  independent QA. One implementation owner edits each code path at a time.
- Default stage budget: at most three specialists, at most two concurrently, one
  debate round and one follow-up per specialist. Expansion requires PI approval.
- Compute budget is not authorized by this plan. Stage 13 must present explicit
  low/medium/high resource envelopes and the recommended choice before training.

## Stop conditions

- `HOLD` on unresolved rights, identity, split leakage, insufficient independent
  units, invalid channel-count coverage or incompatible target labels.
- `HOLD` if numerical/statistical rules cannot be frozen without inspecting
  formal/final results or if matched comparisons cannot be restored.
- `HOLD` if the approved compute envelope cannot complete the frozen matrix.
- `STOP` on final/test leakage, unapproved unseal, corrupted provenance, repeated
  diagnostic failure or pressure to suppress negative/failed runs.
- Stop before training whenever architecture, dataset roles, metrics, claim scope,
  hardware target or compute budget would change without explicit PI approval.

## Planning approval

- Phase objective: approved by PI, 2026-09-30 (Option A).
- Stage decomposition and Stage 11 Charter: `GO` for Stage 11 document-only
  implementation requested by the PI on 2026-10-11 (DEC-072); Stage 11 result
  accepted by the PI under DEC-074. Every later stage remains separately gated.
- No dataset download, code change, training, checkpoint creation or evaluation is
  authorized by this planning document alone.
