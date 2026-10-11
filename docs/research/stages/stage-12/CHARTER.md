# Stage 12 Charter — Data and Evaluation Adequacy

Status: closed

Independent audit QA `PASS`; PI bounded result `GO` (DEC-079).

PI Charter `GO` is recorded in DEC-075. DEC-076 separately approves bounded
access to existing Appliances, Beijing and Bike materials; all other source,
role, split and final/test gates remain pending. DEC-077 separately permits a
shared manifest/notice metadata read for these three sources only.

Proposal baseline: `main` at PR #20 merge
`4aed1926650fe304a818682a718e6b0d608367ba` (2026-10-11).
DEC-074 authorized drafting only. DEC-075 activates this Charter and DEC-076
provides the three named source-access scopes. Neither decision admits a new
source, changes a role or split, or authorizes training, evaluation or a
final/test opening.

## Research question

Do the existing and separately approved candidate public datasets provide
enough independent units, channel-count views and eligible target tasks to
design a leakage-controlled H-01/H-02/H-04 evaluation? Where is the evidence
insufficient, and which source, role and split decisions must the PI make before
Stage 13 can freeze a protocol?

## In scope

- Audit source rights, original/member/manifest hashes, schema, timestamp and
  sampling semantics, missingness, independent units and role boundaries for
  each source within its separately approved access scope.
- Check split-before-windowing, source-range and group disjointness, the
  canonical 512-point purge, and training-only fitted preprocessing. Separate
  originally missing values from observed zero and artificial corruption.
- Audit actual training-seen channel counts and the feasibility of paired
  nested interpolation/extrapolation views, permutation and paired
  0/10/30/50% channel-dropout views without computing model outcomes.
- Prepare an admission packet for each separately approved H-04 candidate:
  rights, labels and task family, ontology, independent subjects/groups, class
  coverage, target-local train/validation and sealed test.
- Recommend `admit`, `reject` or `HOLD` per dataset, with a distinct PI decision
  for source/access, role and split. Give Stage 13 bounded coverage and resource
  estimation inputs, including explicit gaps and unverified claims.

## Out of scope

- Before Charter and source-access `GO`: raw archives, prepared arrays or
  untracked manifests, downloads, conversion and new metadata scans. Before
  approval, only tracked documents, configuration and metadata may be read.
- Throughout Stage 12: Electricity final arrays or model scores; any target
  test arrays, predictions or performance; training, probes and evaluation.
- A new dataset's admission, a change to an existing role/split, or a HAR/HARTH
  repair by trying seeds, splits or metrics after inspecting coverage/results.
- Numerical thresholds, statistical/uncertainty rules, seeds, a run matrix,
  compute envelope, checkpoint selection and protocol-v3 freeze. These belong
  to Stage 13 and its separate PI gate.
- Public release, CUDA or semiconductor validation, or a Q1–Q3 scientific
  qualification. DEC-070 remains `STOP` for publication.

## Inputs and fixed starting roles

- Stage 11 accepted qualification contract, Result and QA; DEC-070–074; the
  Phase 02 plan, hypothesis/requirement/risk registers and Stage 09 `HOLD`/
  final QA `FAIL`. Stage 09 reports and their recorded hashes are immutable.
- `docs/DATASETS.md`, `docs/EXPERIMENT_PROTOCOL.md`, the tracked Stage 06 corpus
  report, and `configs/domain_roles_v1.json` bound to corpus manifest SHA-256
  `44bafe48196a4afd096e387dc672cad128d390ab7e5b413ea6cbeadf5f3e7f6c`.
- Appliances and Beijing: `pretrain`; Bike: `development-held-out`;
  Electricity: sealed `final-held-out`. These are existing roles, not new
  Stage 12 approvals. HAR/HARTH remain unadmitted.
- The tracked Stage 06 report counts 120 split records (85/15/20) and one Bike
  validation record. Split records, windows and repeated seeds are not
  independent source entities. Electricity's tracked metadata is descriptive;
  its final arrays and model scores stay sealed.

## Per-source access request for a later PI decision

The table records each access decision, not a dataset-admission decision. A
`GO` names the source and permitted files/operations before the first read.

| Source | Requested only after Charter GO | Excluded from this request | Decision |
|---|---|---|---|
| Appliances | Existing local official archive/notice, source lock, manifest, and prepared train/validation signals and masks for rights, time, split and view auditing; no model scoring | New mirror/download, role/split change, test signals | `GO` DEC-076 |
| Beijing | Same scope, with station identities, local cadence/gap and missingness checks | New mirror/download, station-transfer claim, role/split change, test signals | `GO` DEC-076 |
| Bike | Same scope, with original entity/range identity and development validation view feasibility | Model selection/evaluation, new final claim, role/split change, test signals | `GO` DEC-076 |
| Electricity | Already tracked documents, registry and corpus-report metadata; DEC-077 permits incidental parsing of shared manifest/notice metadata solely to extract the three approved sources | Raw archive, prepared arrays, final split and model scores; no Electricity adequacy analysis | metadata exception DEC-077 only |
| HAR/HARTH | Already tracked rights and HOLD records only | Raw archive reinspection, signal values, split search, target test | no new access requested |
| New candidate | No candidate selected by this Charter; a later packet must separately request source access and any blinded test-class metadata audit | Download, raw/array read, direct test-label inspection or admission until its own PI decisions | pending candidate-specific request |

For the first three sources, test-range identity and purge may be checked from
approved manifest metadata without opening test signal values. If the packet
needs a broader read, pause and request a narrower additional decision.
DEC-077 resolves the shared-file boundary: only the three approved sources'
rows and notices may enter Stage 12 findings. Electricity metadata encountered
while parsing the shared file is not an approved Electricity audit.

## Ordered work units and deliverables

| Unit | Director/Data deliverable after the applicable gate | Verification and independent QA |
|---|---|---|
| 0 — proposal | This Charter, access-decision requests and corrected PR #20 merge status | Director checks Stage 09 tracked files unchanged and gate wording; independent document-only QA `PASS` and PI Charter `GO` recorded. |
| 1 — access | Per-source purpose, approved bytes/metadata, rights and seal boundary ledger | QA compares every intended read/download with the PI decision before it occurs. Unapproved sources remain `HOLD`. |
| 2 — provenance | Per-source official URL/DOI, terms and bundled notices, archive/member/manifest/registry hashes, schema, channel and time/missingness facts | QA independently rechecks recorded hashes and notices within approved access; discrepancies become `HOLD`, never silent substitutions. |
| 3 — independence | Separate record, original entity/subject and nonoverlapping time-range counts; split, purge, preprocessing and role-leakage audit | QA checks identity and range overlap, source split before windows, 512-point purge and train-only fitted state; no window or seed count is used as sample size. |
| 4 — views | H-01/H-02 feasibility grid by source, split and seen/unseen count, with paired-view and mask eligibility | QA checks same-record nested channels, common observed targets/reference, permutation alignment and clean/dropout comparability. No model score is generated. |
| 5 — target/handoff | Admission packet for each approved H-04 candidate; dataset decisions, insufficiencies and Stage 13 resource inputs | QA checks rights, ontology, independent groups, per-split class coverage and test seal, then reports `PASS`, `CONDITIONAL PASS` or `FAIL`. PI decides each source/role/split and the Stage 12 result. |

The Director writes tracked packets and the result; Data supplies bounded source
and split evidence; QA is independent and edits no tracked evidence. A candidate
with an unresolved gate is documented as `HOLD`, not treated as admitted.

## Audit record and decision form

For every field below, record `confirmed`, `unverified` or `conflict` and an
exact evidence pointer. `—` is an unfilled field, not an approval.

| Dataset | Starting role | Source/rights/hashes | Schema/time/missingness | Independent record/entity/ranges | Split/purge/preprocessing/leakage | H-01/H-02 views | H-04 target | Proposal |
|---|---|---|---|---|---|---|---|---|
| Appliances | pretrain | — | — | — | — | — | — | — |
| Beijing | pretrain | — | — | — | — | — | — | — |
| Bike | development-held-out | — | — | — | — | — | — | — |
| Electricity | sealed final-held-out | tracked metadata only | tracked metadata only | sealed | sealed | sealed | — | — |
| HAR / HARTH | unadmitted | — | — | — | — | — | — | HOLD |
| One row per new candidate | unapproved | — | — | — | — | — | — | — |

| Separate PI decision | Available dispositions | Proposed default pending evidence |
|---|---|---|
| Charter and each source's audit access | `GO` / `REVISE` / `HOLD` | Approve the smallest useful source-specific scope; do not infer access from the Charter alone. |
| Source admission and rights | `admit` / `reject` / `HOLD` | Keep unreviewed sources `HOLD`; preserve existing Stage 06 history. |
| Role | keep / approve a versioned change / `HOLD` | Keep the four current roles; no role change from a measurement alone. |
| Split | keep / approve a versioned proposal / `HOLD` | Keep or `HOLD`; no performance- or coverage-driven seed search. |
| H-04 target | `admit` / `reject` / `HOLD` | Admit only with complete target-local and sealed-test evidence. |

The PI decision record must name the source, access scope, intended role,
split identity, rights basis and any exclusions. New admissions or role/split
changes update a versioned registry/manifest only after that decision.

## Hypothesis adequacy and HOLD rules

- **H-01:** derive seen counts from actual training manifests and sampling,
  not nominal source channel totals. Separate unseen interpolation from
  extrapolation. For each eligible count, require deterministic nested views
  of the same source record, common valid observed target coordinates, and
  aligned channel/mask permutation. Unpaired datasets are descriptive only.
  Insufficient independent sources or paired views make that coverage `HOLD`.
- **H-02:** distinguish source missingness, padding, hidden targets and
  artificial channel dropout. Require identical source record and shared
  target/reference coordinates for the 0/10/30/50% views, including a clean
  cross-arm comparison. If any registered rate lacks comparable valid targets
  or evidence depends on repeated windows of one entity, mark it insufficient.
- **H-04:** record rights and notices, label/task family, registered ontology,
  independent subject/group counts, class coverage in train/validation and the
  status of test-class coverage without direct test-label or test-array access,
  target-local train/validation and sealed test, and exclusion from encoder
  pretraining/calibration. HAR retains its README rights conflict. HARTH retains
  absent bundled notice, S006 10 ms subject cadence versus 50 Hz description,
  and official class 14 missing from the fixed candidate test split. Do not
  repair these by result- or coverage-informed seed/split/metric search.
  Without an admitted target H-04 is `not tested` and Q2/Q3 are unavailable;
  separately approved Electricity-only readiness can still proceed later.

Test-class coverage may be cited only from already tracked, approved metadata
or a separately PI-authorized blinded metadata-only audit that returns fixed
class-presence/count summaries without exposing test labels or signals to the
model/evaluation team. Otherwise mark coverage `unverified` and admission
`HOLD`; Stage 12 does not unseal target test to complete the packet.

No adequacy finding itself establishes Q2 coverage. Stage 13 must preregister
minimum coverage and inference rules before formal results; Stage 19 assigns
the actual evidenced Q level.

## Stage 13 handoff

Deliver per-source `admit`/`reject`/`HOLD` recommendations and PI source/role/
split decisions, independent units and usable views, possible bounded domain/
task/channel claims, missing evidence and needed additional data. Provide only
resource-estimation inputs: approved data bytes, sequences and channel ranges,
usable independent records, feasible view counts, expected I/O/preprocessing,
candidate hardware and known uncertainty. Window counts may size processing
work, never statistical sample size. Stage 13 owns low/medium/high budgets,
seeds, arms, steps, thresholds, uncertainty, checkpoint selection and freeze.

## Acceptance criteria

- [ ] Charter and source-access gates are recorded separately; no unapproved
  source, raw/array, Electricity final or target-test access occurred.
- [ ] Every audited source has a rights/provenance/schema packet with exact
  evidence or an explicit `unverified`/`conflict` status.
- [ ] Original entities/subjects, split records and disjoint ranges are
  distinguished; purge, split order, preprocessing and role leakage are checked.
- [ ] H-01/H-02 coverage is supported by eligible paired views or explicitly
  limited; no synthetic view or repeated seed is called empirical coverage.
- [ ] Every considered H-04 target has a complete admission packet or `HOLD`;
  HAR/HARTH blockers and sealed tests are preserved.
- [ ] Stage 13 receives decision points, claim limits, insufficiencies and
  resource inputs without a Stage 12 numerical or compute freeze.
- [ ] Independent QA reports a verdict; governance/notebook/diff checks pass;
  Stage 09 tracked reports and their historical hashes/verdict are unchanged.

## User checkpoints

| Gate | Required before | Current state |
|---|---|---|
| Stage 12 Charter | Any Stage 12 data work or specialist data audit | `GO`, DEC-075 |
| Per-source access, including existing raw/prepared corpus | Any read beyond tracked documentation/metadata or download | Appliances/Beijing/Bike `GO` within DEC-076; shared metadata exception DEC-077; other access pending |
| Source admission, role and split | New use or a registry/manifest change | DEC-078 approves named bounded A/B/B uses with existing roles/splits; all expansions pending separately |
| Stage 12 result | Stage 13 work beyond a proposal | bounded `GO`, DEC-079; Stage 13 Charter/protocol/compute still pending |
| Final/test opening | Electricity or target-test evidence | outside Stage 12; pending Stage 17 PI gate |

## Agent plan and budget

- Research Director: Charter, decisions, packets, notebook and stage-gate report.
- Data specialist: only after Charter/access `GO`, bounded source, rights, schema,
  identity, split and view audit; read-only research role.
- Independent QA Engineer: document-only proposal review now; later independent
  recheck of approved evidence and access ledger, without tracked-file edits.
- Experiment specialist: conditional only for a material H-01/H-02 feasibility
  dispute; activation or expansion requires a Charter/PI budget decision.

```yaml
agent_budget:
  default_mode: single_agent_until_charter_go
  max_specialists: 2
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 1
  max_agent_report_words: 700
  user_approval_for_expansion: true
```

Provisional post-approval labor estimate: 2–4 Director/Data person-days plus
1–2 independent QA person-days, excluding rights or source-access delays.
Stage 12 authorizes no GPU run or training budget. CPU I/O estimates await the
approved source locations and scope; Stage 13 estimates formal compute.

## Risks and stop conditions

- `HOLD` on unresolved rights or notice, source/hash mismatch, identity/split
  overlap, insufficient independent units, invalid channel pairs or H-04 labels.
- `HOLD` on any material change to source eligibility, role, split, claim scope
  or agent/compute budget without the corresponding PI decision.
- `STOP` on final/test leakage, unapproved access, corrupted provenance or
  attempted result-driven split/seed/metric search. Preserve the failed evidence.
- Stage 09 `HOLD`/QA `FAIL` and both report hashes remain historical. DEC-070
  prohibits tag, release/prerelease, PyPI and public checkpoint publication.

## User approval

- Decision: `GO` for this Stage 12 Charter (DEC-075).
- Date: 2026-10-11.
- Conditions: DEC-076 separately names the three approved access scopes.
  Charter `GO` does not replace admission, role, split or later stage gates.
- Closure: independent Stage 12 audit QA `PASS`; DEC-078 decides the three
  bounded source uses with unchanged roles/splits and DEC-079 accepts the
  bounded adequacy result. No later stage or final/test gate is implied.
