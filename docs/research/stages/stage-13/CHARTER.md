# Stage 13 Charter proposal — Protocol v3 and Compute Budget Freeze

Status: approved

PI Charter `GO` was granted on 2026-10-11 (DEC-082), after independent
document-only QA `PASS` and Draft PR #23 review. This activates the bounded
Charter; it does not approve candidate discovery, source access/admission,
role/split changes, a protocol, compute budget, training, evaluation or
final/test opening.

Proposal baseline: PR #21 merged at
`f83f8941afb0a7859043253dc5c4251d953bed56`; PR #22 merged into `main` at
`392b7853cf5e6ef022ab943fb8e6dd3481d13e7d` on 2026-10-11. DEC-079
accepted the bounded Stage 12 handoff. DEC-081 records the PI's new-data-first
planning direction and request for this proposal, without Charter `GO`.

Proposal review: independent document-only QA **PASS** on the Charter and
research-state/gate corrections. This is not protocol pre-freeze QA or a PI
Charter decision; it checked no candidate, array, model result or budget.

## Research question

Can an independently held-out public corpus and a feasible matched compute
envelope support a pre-result protocol v3 for H-01–H-03 with valid paired
channel-count, dropout and topology endpoints? If not, which prerequisite is
missing and why must the freeze remain `HOLD`?

## Eligibility and claim boundary

Appliances and Beijing retain their approved `pretrain` roles and chronological
splits. Bike retains `development-held-out` for dimensionless diagnostics.
Electricity remains sealed `final-held-out`. Training-seen channel counts are
11 and 26. Bike has four channels and one original entity, so its validation
data cannot make a same-record nested view against nearest seen count 11.
Bike's 71 train fragments, windows and repeated seeds are not independent
units. Beijing's 12 stations share city and time and need dependence review.
Appliances/Beijing views from training-seen entities are diagnostics, not
independent held-out count evidence. Bike 10% dropout can remove zero channels;
its `temp` physical units and inverse remain unresolved.

No H-04 target is admitted. HAR/HARTH retain their recorded `HOLD` reasons;
H-04 is `not tested` and Q2/Q3 are unavailable. Stage 11's Q0–Q3 contract is
not an experimental result. The existing three sources do not permit a full
H-01–H-03 protocol-v3 freeze under that contract. The PI selected a new-data-
first planning path, not candidate access. If no eligible source is admitted,
close the freeze attempt at `HOLD`. A narrower H-01/Q1 contract requires a new
PI decision; thresholds or sample sizes cannot be changed to hide the gap.

## In scope after Charter GO and the applicable additional gates

- Request a bounded, metadata-only public candidate search from the PI before
  discovering a new source. Then prepare a named candidate-specific access
  request. Only after its PI access `GO`, audit source rights, archive/member
  hashes, schema, time/missingness, original entities and dependent periods,
  split/purge, roles and paired views. Source admission, role and split each
  require distinct PI decisions.
- On admitted sources, propose separate H-01 permutation, interpolation and
  extrapolation endpoints; H-02 effective integer dropout, paired target and
  reference, clean harm and missingness; and both H-03 topology contrasts.
  Define primary, secondary and diagnostic outcomes separately.
- Fix original entity/time-aware aggregation, paired graph/training-seed
  hierarchy, numerical guards, minimum effects, adverse harm, uncertainty,
  multiplicity, missing/failed-run handling and claim limits before results.
  Review only general H-04 target-local packet rules for Stage 17 binding.
- Present low/medium/high compute envelopes with arms, seed/run counts, steps,
  exposure, setup/I/O, training, validation, evaluation, checkpoint, memory,
  disk, exact environment, estimator uncertainty and failure allowance.
  Non-final or synthetic measurements need their own stated PI gate.
- Prepare versioned protocol/config/matrix/analysis and a byte-hashed freeze
  manifest. Address Windows registry LF/CRLF checkout with a byte-exact rule
  and pre-load raw-hash check, preserving historical registry/manifest hashes.
  Make only justified v3 evaluator, validator, runner and reporter changes.

## Out of scope and access boundary

- Before Charter `GO`: work beyond tracked-document/code/config/metadata
  review, proposal writing and a Charter Draft PR. Charter `GO` alone does not
  permit candidate search, new-source download, raw/prepared array reading,
  role/split changes, model training/evaluation, checkpoint creation or
  compute expenditure.
- Throughout Stage 13: Electricity raw/prepared/final signals or model scores,
  any test signal/score, target probe/test execution, formal training or
  evaluation, final opening, publication, CUDA support claims and semiconductor
  transfer. Stage 14 synthetic preflight and Stage 15 execution have later gates.
- Any retrospective change to Stage 09 `HOLD`, final QA `FAIL` or report hashes.
  Its unfrozen five-seed/60-run proposal and numerical candidates are not v3
  defaults. DEC-070 public-release `STOP` remains in force.

## Ordered work units

| Unit | Deliverable and owner | Independent check or gate |
|---|---|---|
| 0 — proposal | Director: this Charter, current-state and merge corrections, Draft PR. | Document-only independent QA; PI Charter `GO`/`REVISE`/`HOLD` before Unit 1. |
| 1 — eligibility | Director/Data if activated: separately approved metadata-only candidate search, then per-source access request, admission packet, source/role/split decisions and endpoint grid. | QA checks each search/access authorization, rights, hashes, entities, ranges, seal and paired views. No admission or count coverage means freeze `HOLD`. |
| 2 — endpoints | Experiment/Director: v3 protocol and analysis proposal for permutation/count/dropout/clean harm and both topology controls. | QA checks shared target/reference, dependence, inference and claim bounds. |
| 3 — matrix/budget | Experiment/Integrator: versioned config/matrix, low/medium/high envelopes and one recommended PI option. | QA checks single-factor matching, parameters, steps/exposure, environment and phase costs. |
| 4 — tooling | One implementation owner: minimum v3 evaluator/validator/runner/reporter changes and synthetic tests. | QA checks roles/seals, actual record sufficient-statistic contract, declared-input-only replay, aliases, nonfinite failures, resume and hashes. |
| 5 — freeze review | Director: complete v3, budget, freeze manifest, Result/QA and notebook/traceability/risk changes. | Independent pre-freeze QA `PASS`, then explicit PI protocol and selected-budget `GO`; otherwise `HOLD`. |

Units 1–5 are conditional work, not authorized by the request to draft this
Charter. A failed candidate is not silently replaced; another candidate needs
its own packet. A material change after freeze requires v4 and PI review.

## Acceptance criteria and Stage 14 handoff

- [ ] Every used source has PI-approved access, rights, role and split; source,
  manifest, registry and worktree bytes check without changing history.
- [ ] H-01 held-out paired count, H-02 effective corruption and both H-03
  matched contrasts have eligible observations and explicit independent-unit
  limits.
- [ ] Protocol v3 fixes endpoints, integer masks, references, aggregation,
  seed hierarchy, guards, effects, uncertainty/multiplicity, checkpoint
  selection, failure/diagnostic rules and full matrix before outcomes.
- [ ] Low/medium/high options specify arm/seed/run structure, steps, exposure,
  FLOPs and wall time separately, phase costs, memory/disk, exact environment,
  measurement basis/error and failure allowance; PI selects one.
- [ ] Frozen files and source/code/environment hashes replay exactly;
  adversarial synthetic checks and independent pre-freeze QA return `PASS`.
- [ ] PI explicitly approves exact protocol and budget. Only then may a
  separately gated Stage 14 synthetic/tiny preflight begin. Stage 15 training
  additionally needs Stage 14 QA and PI execution `GO`.

Insufficient independent count coverage, unresolved rights/split, invalid
H-02 views, unmatched controls, infeasible cost, incomplete provenance or
non-`PASS` QA leaves Stage 13 at `HOLD` and blocks freeze. A valid negative
result is a later scientific outcome, not a reason to rewrite this design.

## User checkpoints

| Decision | Required before | State |
|---|---|---|
| Stage 13 Charter `GO`/`REVISE`/`HOLD` | Units 1–5, subject to their additional gates | `GO`, DEC-082 |
| Bounded metadata-only candidate search | Any search for a new source | `GO`, DEC-083; at most three official-document candidates |
| Candidate access, then source/use, role and split | First access/admission or change for each named source | PhysioNet sidecars `GO` DEC-084, six headers `GO` DEC-085, six full in-memory EDF streams `GO` DEC-087 and three audit-only subject exclusions `GO` DEC-088; source/use admission, development role and formal split pending |
| Non-final/synthetic resource measurement, if needed | That measurement | pending |
| Exact v3 and selected compute envelope `GO` | Freeze/Stage 14 handoff | pending |
| Stage 15 execution; Stage 17 H-04/final opening; publication | Separate later stages | pending; publication `STOP` DEC-070 |

## Bounded candidate discovery — PI GO (DEC-083)

Search at most three official public dataset landing pages and their linked
license, schema and documentation pages for a development-held-out candidate.
Record only publisher-stated rights, original entity/group count and dependence,
native channel count and ordering, cadence/missingness, available time/group
split information, and whether same-record nested seen/unseen views appear
possible. Prioritize a source with at least 11 genuine channels; upper-count
extrapolation beyond the currently seen maximum 26 requires at least 27.
These are screening criteria, not admission or a promise of statistical power.

This request excludes archives, downloads, mirrors, sample tables, raw or
prepared arrays, test labels/signals/scores, model outputs, and performance-
based candidate ranking. The output is a short metadata-only shortlist with
`confirmed`/`unverified`/`conflict` fields and source links. Each named
candidate's first deeper read/download, source/use, role and split still need
separate PI decisions. DEC-083 authorizes only the metadata-only search above.

## Agent plan and budget

The Research Director owns decisions, Charter, handoff and tracked records.
After Charter `GO`, activate Experiment for endpoint/statistical design and
Program Integrator for scope/budget/gate consistency. Activate Data for a
separately authorized candidate admission when needed. Independent QA reviews
the proposal and exact pre-freeze packet; QA edits no tracked files. One
implementation owner edits a code path at a time. Specialists do not delegate.

```yaml
agent_budget:
  default_mode: single_agent
  max_specialists: 6
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 2
  max_agent_report_words: 700
  user_approval_for_expansion: true
```

Compute budget: **unapproved**. No numerical threshold, seed identity,
formal matrix, checkpoint policy or low/medium/high option is frozen here.

DEC-086 approved this staffing ceiling after the original Charter. Three
specialists and one follow-up each were already used; at most three additional
conditional specialists and one further follow-up per existing reviewer are
available. Parallelism remains two agents. This amendment authorizes no source
access, role/split, protocol or compute decision.

## User approval

- Specialist-budget amendment: `GO`, DEC-086, for the bounded ceiling above.
  All source, role/split, protocol, compute and execution gates remain separate.
- Charter decision: `GO`, DEC-082.
- Candidate discovery decision: `GO`, DEC-083, on the bounded request above.
- PhysioNet sidecar-only access: `GO`, DEC-084; see
  [inventory](PHYSIONET_SIDECAR_AUDIT.md). Source/use admission, role, split and
  all deeper source access are pending by named candidate.
- Six EDF headers only: `GO`, DEC-085; see the approved
  [request](PHYSIONET_HEADER_PILOT_REQUEST.md). This is not source admission.
- Six bounded in-memory EDF streams: `GO`, DEC-087, separately from the
  S001/S055/S109 audit-only exclusion `GO`, DEC-088. The approved
  [signal-audit request](PHYSIONET_SIGNAL_AUDIT_REQUEST.md) allows no other
  source, model or test access. Source/use admission and formal split remain
  pending.
- Protocol and compute decision: pending after independent pre-freeze QA.
