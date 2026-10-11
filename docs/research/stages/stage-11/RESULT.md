# Stage 11 Result — Foundation Qualification Contract

Status: contract drafted; independent QA `PASS`; PI result gate pending

Date: 2026-10-11

## Decision basis and historical boundary

- Baseline is local/remote `main` at PR #19 merge
  `52fd44af0145e19d5f26138382bb0661e975eb09`, tree
  `618a9504ce6d10b2374f906613b3e91f2e0589f8` (DEC-072).
- DEC-071 approved the falsifiable Phase 02 objective. DEC-072 authorized only
  Stage 11 document work. Stage 11 result acceptance and Stage 12 work remain
  separate PI decisions. DEC-070 still prohibits public release.
- Stage 09 closed at `HOLD` under DEC-058, with DEC-057 final reporter QA `FAIL`.
  Preserved `REPORT.json` and `REPORT-v2.json` SHA-256 values are
  `1bb8c7f9d1811ee0caceaaabbb65f146ee892e2f0e84bb88433fb5b844e5b520`
  and `8ab632b54e36c22ee7bc89212e53904092dba3cfa6e8fc0bc29a7285b4760db3`.
  H-01–H-03 have no formal result; H-04 is `not tested`. The Stage 09 five-seed,
  60-run v2 matrix and Stage 01 numerical candidates were never frozen for this
  phase. Stage 10 CPU/offline engineering QA informs Q0 only.
- `docs/EXPERIMENT_PROTOCOL.md` and `docs/DEVELOPMENT_PLAN.md` retain historical
  Stage 01/09/10 language. The prospective Phase 02 contract and later approved
  protocol v3 govern new formal work. No old stage reference grants access.

## Qualification result and negative paths

The contract in `docs/research/PHASE_02_FORMAL_VALIDATION_PLAN.md` distinguishes
Q0 engineering operation, Q1 valid frozen H-01–H-03 formal evaluation, Q2 bounded
foundation-encoder evidence requiring registered H-01/H-02 and admitted-target
H-04 support, and Q3 the additional H-03 advantage against both matched controls.
Q1 records valid outcomes even when they are `no-support`, `harm` or
`inconclusive`; it does not assert model quality. With no admitted H-04 target,
Q2/Q3 are unavailable. One favorable H-03 contrast cannot establish Q3.

Valid negative, inconclusive and infeasible outcomes remain reportable results.
An infeasible or invalid formal path ends at `HOLD`/`STOP`, names untested
hypotheses and awards no unsupported Q level. The actual Q level is deferred to
Stage 19; current scientific support for foundation quality, topology advantage,
transfer, CUDA and semiconductor suitability is `미검증`.

## Prospective Stage 12–19 handoff audit

| Stage | Required input and evidence owner | Independent check and PI boundary | HOLD/STOP or skip path |
|---|---|---|---|
| 12 — adequacy | Stage 11 contract; Data measures rights, schema, time/missingness, independent units, disjoint ranges/groups, channel views and conditional target-label suitability. | Data/QA admission packets; separate PI Charter/data-access and each source/role/split decision. | `HOLD` on rights, leakage, inadequate units/views or labels. H-04 stays `not tested` without an admitted target. |
| 13 — protocol/budget | Stage 12 approved roles and measured adequacy; Experiment/Program Integrator present protocol v3 plus low/medium/high budgets. | Independent pre-freeze QA `PASS` and explicit PI endpoint, statistics, matrix and compute `GO`; freeze hash precedes formal results. | `HOLD` if rules or matched controls cannot be frozen within an approved envelope. |
| 14 — preflight | Frozen protocol and selected budget; Implementation rehearses runner, reporter, cache, resume, provenance, no-network and failure paths on blind/synthetic inputs. | Independent QA `PASS`; exact CUDA environment validation if CUDA is proposed. | `HOLD` on resource overrun or nonreproducible/unsafe paths. No formal/final evidence. |
| 15 — formal training | Stage 14 evidence, frozen H-01–H-03 matrix and separate PI execution `GO`; Experiment owns exact runs and failure ledger. | QA checks actual inputs, matching, steps, exposure and provenance. | Preregistered diagnostic rule or `HOLD`/`STOP`; no adaptive seeds/arms/runs. |
| 16 — development analysis | Valid Stage 15 runs; Experiment applies frozen analysis and development-only selection policy. | Independent QA `PASS` and PI outcome/candidate decision. | At most one private candidate, or explicit no-candidate result; without one skip final execution. |
| 17 — final readiness | Selected candidate and Stage 13 general rules; Data/Experiment audit the sealed Electricity ledger, and bind target-specific ontology/split evidence only if H-04 is pursued. | Independent QA and separate PI `GO` for H-04 and/or one-time Electricity/target-test opening. | A missing H-04 target keeps H-04 `not tested` but does not block separately approved Electricity readiness; a missing candidate or failed readiness keeps final assets sealed. |
| 18 — one-time final | Approved Stage 17 access and locked candidate; Experiment records atomic open, predictions and sufficient statistics once. | Independent QA and PI outcome acceptance. | Invalid access/provenance is `STOP`; no automatic rerun, tuning or reranking. |
| 19 — closeout | All valid and skipped outcomes; Director maps evidence to Q0–Q3 and private checkpoint disposition. | Independent QA and PI `GO`/`HOLD`/`STOP` on phase result. | Negative or infeasible result may close the research question; public release needs another decision. |

The hypothesis and R-01–R-12 owner-level crosswalks are in `HYPOTHESES.md` and
`REQUIREMENTS_TRACEABILITY.md`. R-08 semiconductor work follows only a separate
post-Phase 02 PI decision. Existing R-06 CPU and R-07 offline evidence remains
environment-bound and does not imply CUDA validation or future offline readiness.

## Handoff packet without admission or budget choice

Stage 12 must make independent records/entities/ranges and leakage measurable;
check rights, source/checksum, time and missingness semantics, purge and train-only
preprocessing; establish seen/unseen channel-count coverage and paired
interpolation/extrapolation views; and audit H-04 label/task-family, ontology,
group-disjoint split and target-test seal. It may recommend admission decisions
but may not infer them from this result. Appliances/Beijing pretrain, Bike
development-only and Electricity sealed final-held-out remain starting roles.

Stage 13 must present low/medium/high options with arm/run and seed structure,
steps/exposure, setup/training/validation/evaluation/checkpoint time, memory/disk,
hardware/software environment, estimator uncertainty, failure allowance and
claim coverage. It separates optimizer steps, wall time and FLOPs. No option,
dataset, numerical threshold, statistical rule, seed or run matrix was selected
by Stage 11.

## Stage 11 verification and disposition

Program Integrator read-only review identified historical/prospective reference
drift, the premature Stage 11 envelope-selection gate and the Stage 17/18 opening
reference. The contract, hypothesis/requirement maps and risk controls now address
those points. Independent QA records its own verdict in `QA_REPORT.md`.

The independent QA first found two stale/ambiguous gate lines; its first delta
review verified those corrections and found one related Result line. The Director
corrected the final line, and the PI authorized one additional bounded independent
review (DEC-073). QA returned `PASS` on exact PR head `0effe407`. `QA_REPORT.md`
preserves the initial conditional reviews and the final verdict.

Stage 11 cannot authorize Stage 12 data work. After QA, the PI must decide whether
to accept this result and whether a Stage 12 Charter may be drafted. A later
Stage 12 Charter/data-access `GO` is still required before data work.

Draft PR #20 (`codex/stage-11-qualification-contract`) presents the document-only
packet for review (initial commit `b15b769`); it is not merged or a Stage 11 result
decision.

Director final-diff checks on 2026-10-11: `python
tools/validate_research_governance.py`, `python
.agents/skills/flyts-lab-notebook/scripts/check_notebook.py`, `git diff
--check`, `git diff --exit-code main -- docs/research/stages/stage-09`, and a
focused read of the corrected Stage 17 rows and approval line all passed. The
separate DEC-073 QA review independently confirmed the corrected contract.
