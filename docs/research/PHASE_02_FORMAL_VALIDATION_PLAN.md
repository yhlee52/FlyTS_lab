# FlyTS Phase 02 — Formal Training and Scientific Evaluation

Status: proposed stage plan; phase objective approved by the PI

Decision basis: DEC-071, 2026-09-30

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

Q2 and Q3 thresholds, minimum domain/task coverage and uncertainty rules must be
fixed in Stages 12–13 before formal results. This phase cannot establish a
universal foundation-model, production, CUDA or semiconductor claim.

If H-01/H-02/H-04 support but H-03 does not, evidence may support the
channel-agnostic encoder but not a connectome-specific advantage. If H-04 cannot
be admitted, Q2/Q3 are not reached and H-04 remains `not tested`.

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
| 11 — Qualification contract | Turn the approved objective into falsifiable qualification levels, hypotheses, claim boundaries, stage ownership and compute-envelope options. | Stage Charter, qualification matrix, updated traceability and risks, phase budget options. | PI `GO` on the Stage 11 result and chosen compute/data planning envelope. No training. |
| 12 — Data and evaluation adequacy | Determine whether existing and candidate public domains provide enough independent records, channel-count coverage and eligible target tasks without leakage or rights ambiguity. | Dataset admission packets, role/split manifests, independent-unit audit, H-01/H-02 coverage analysis and H-04 target decision. | PI approves every new source/role/split; otherwise `HOLD` or reduce the registered claim set. |
| 13 — Protocol v3 and budget freeze | Freeze endpoints, guards, minimum effects, uncertainty/multiplicity rules, seeds, comparison arms, checkpoint selection, run matrix and compute budget before formal results. | Hashed protocol v3, configs, run matrix, statistical analysis plan, compute estimate and freeze manifest. | Independent pre-freeze QA `PASS` plus explicit PI protocol/budget `GO`. Any later change creates v4. |
| 14 — Execution preflight | Prove that the frozen runner, reporter, cache, checkpoint, resume and failure paths work end to end without using formal/final evidence. | Synthetic/tiny blind rehearsal, runtime/memory evidence, deterministic manifests, no-network test and preflight QA report. | QA `PASS`; predicted resources fit the approved envelope. CUDA use requires a separately validated exact environment. |
| 15 — Formal multi-seed training | Execute the frozen H-01–H-03 matrix without adaptive changes, result-driven stopping or added runs. | Local checkpoints, run manifests, logs, failure ledger, exact exposure/compute records and sealed evaluation inputs. | All planned runs are valid, or the preregistered failure/diagnostic rule yields `HOLD`/`STOP`. No final-held-out access. |
| 16 — Development evaluation and selection | Apply the frozen analysis plan, issue bounded H-01–H-03 outcomes and select at most one private checkpoint using development evidence only. | Locked report, sufficient statistics, hypothesis outcomes, selection ledger and checkpoint provenance. | Independent QA `PASS`; PI accepts the outcomes and either one candidate or an explicit no-candidate result. |
| 17 — Transfer/final readiness | If Stage 12 admitted a target, freeze H-04 probe controls and audit the selected checkpoint plus one-time final orchestration. | Target protocol, ontology/split evidence, final access ledger, unseal rehearsal and readiness QA. | Separate PI `GO` for H-04 execution and/or the one-time final open. Missing prerequisites keep H-04 `not tested`. |
| 18 — One-time final evaluation | Evaluate the already selected checkpoint once on the frozen final/target evidence; never tune, rerank or add runs from the result. | Atomic unseal record, final predictions/sufficient statistics, locked report and independent QA. | PI accepts `support`, `no-support`, `harm`, `inconclusive` or invalid/stop outcome. No automatic rerun. |
| 19 — Phase closeout | Map all valid outcomes to Q0–Q3, decide private checkpoint retention and record limitations and the next research decision. | Final evidence matrix, model card update, private checkpoint disposition, phase result and QA report. | PI `GO`, `HOLD` or `STOP`. Publication remains a separate future decision and defaults to no release. |

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
- H-01–H-03 each receive a bounded outcome rather than an implied positive claim;
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
| Phase stage plan and Stage 11 Charter | Beginning Stage 11 implementation | pending PI review |
| Dataset admission/role/split | Using any new domain or changed role | pending per Stage 12 proposal |
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
- Stage decomposition and Stage 11 Charter: pending PI `GO`.
- No dataset download, code change, training, checkpoint creation or evaluation is
  authorized by this planning document alone.
