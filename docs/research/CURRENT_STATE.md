# FlyTS Current Research State

Updated: 2026-10-11

## Current stage

Stage 09 closed at PI-accepted `HOLD` (DEC-058) with final reporter QA `FAIL`
(DEC-057); H-01–H-03 have no formal result and H-04 is `not tested`. Stage 10
CPU/offline engineering did not override DEC-070 public-release `STOP`.
Stage 11's qualification contract received independent QA `PASS` and PI `GO`
(DEC-074); PR #20 merged at `4aed192`. Stage 12 closed with independent QA
`PASS` and bounded PI `GO` (DEC-079); DEC-078 kept three existing roles and
splits. PR #21/#22 merged at `f83f894`/`392b785`. The Stage 13 Charter has
document-only QA `PASS` and PI `GO` (DEC-082); Draft PR #23 remains unmerged.
Electricity and all target test signals/scores remain sealed.

## Current goal

Prepare a bounded metadata-only candidate-discovery request for PI review.
DEC-081 sets the new-data-first path; DEC-082 approves the Charter alone.
Candidate search/access/admission, protocol and compute remain separately gated.

## Canonical references

- `docs/research/PHASE_02_FORMAL_VALIDATION_PLAN.md`
- `docs/research/stages/stage-11/CHARTER.md`
- `docs/research/stages/stage-11/RESULT.md`
- `docs/research/stages/stage-11/QA_REPORT.md`
- `docs/research/stages/stage-12/CHARTER.md` (closed; DEC-075–079)
- `docs/research/stages/stage-12/ADEQUACY_PACKET.md` (bounded evidence)
- `docs/research/stages/stage-12/RESULT.md` (QA PASS; PI GO)
- `docs/research/stages/stage-12/QA_REPORT.md` (independent audit PASS)
- `docs/research/stages/stage-13/CHARTER.md` (approved; DEC-082)
- `docs/research/DECISION_LOG.md` (DEC-070–082)
- `docs/research/HYPOTHESES.md`
- `docs/research/REQUIREMENTS_TRACEABILITY.md`
- `docs/research/RISK_REGISTER.md`
- `docs/research/stages/stage-09/RESULT.md`
- `docs/research/stages/stage-09/QA_REPORT.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/DEVELOPMENT_PLAN.md`

## Confirmed decisions

- The PI is the final `GO`, `REVISE`, `HOLD` or `STOP` authority. DEC-072 covers
  only Stage 11 documentation, Program Integrator review and independent QA.
- Q0 means bounded CPU engineering operation; Q1 requires valid frozen H-01–H-03
  evaluation; Q2 additionally needs registered H-01/H-02 and admitted-target
  H-04 support; Q3 additionally needs H-03 support against both matched topology
  controls. These are PI-accepted Stage 11 qualification rules, not achieved
  scientific claims; later eligibility and numerical rules remain gated.
- Stage 09's `HOLD`, QA `FAIL`, reports/hashes and unfrozen v2 matrix are historical.
  Prospective Stage 10 reporter hardening does not retrospectively repair them.
- Appliances/Beijing remain pretrain, Bike development-only and Electricity
  sealed final-held-out. HARTH remains unadmitted. Stage 11 changes no role,
  split, metric, numerical rule, seed, run matrix or compute budget.
- Stage 12 must measure adequacy and seek separate source/role/split decisions;
  Stage 13 must offer low/medium/high budgets and seek protocol/compute `GO`.
  Stage 15 execution and Stage 17 H-04/final opening have further distinct gates.
- DEC-070 prohibits tag, GitHub release/prerelease, PyPI and checkpoint
  publication. Package `flyts 0.2.0` and research artifact `v0.1` remain distinct.
  Existing Stage 10 CPU/offline evidence has no CUDA or scientific inference.
- DEC-073 authorized one additional independent QA review beyond the Stage 11
  follow-up limit; QA returned `PASS` on PR #20 head `0effe407`. This is not
  itself a Stage 11 result decision. DEC-074 separately records PI result `GO`:
  Stage 12 Charter drafting was authorized. PR #20 later merged, but Stage 12
  data access, admission and role/split decisions were unapproved at that time.
- DEC-075 approved the Stage 12 Charter. DEC-076 separately permits existing
  local Appliances, Beijing and Bike official archives/notices, source lock,
  manifest and prepared train/validation signals/masks for bounded audit only.
  Test signals, Electricity raw/prepared/final, HAR/HARTH raw data, downloads,
  model scores and role/split changes are outside this approval.
- DEC-077 allows bounded shared manifest/notice metadata reads for the three
  approved sources, without an Electricity adequacy audit or final opening.
- DEC-078 admits Appliances/Beijing for existing bounded uses with pretrain
  roles/current splits; Bike retains development role/split for dimensionless
  diagnostics only. Bike H-01 count coverage and `temp` semantics stay `HOLD`.
  DEC-079 accepts the bounded Stage 12 result, not Stage 13 execution.
- DEC-080 separately authorizes merging the two Stage 12 PRs; it changes no
  scientific or release gate.
- DEC-081 chooses new-data-first planning and requests a Charter proposal;
  it grants no Stage 13 or data access approval.
- DEC-082 approves the Stage 13 Charter, not candidate discovery/access,
  admission, protocol/budget freeze, execution, final opening or PR merge.

## Open questions

- Candidate discovery/access/admission, minimum coverage, statistical
  thresholds, seed/matrix, budget, H-04 target, CUDA and final open remain gated.

## Active risks

- RK-08, RK-33 and RK-51–55: final/test leakage, pseudo-replication, selection
  leakage, post-result scope expansion, compute infeasibility and historical
  Stage 09 or Stage 11 gates being misread as new authority.
- H-04 can remain `not tested`; without an admitted target Q2/Q3 are unavailable.
  A valid negative, inconclusive or infeasible result is still a research result.
- CUDA hardware remains unvalidated; CPU evidence cannot establish CUDA behavior.
  Public release remains stopped despite Stage 10 engineering QA `PASS`.

## Latest evidence

- Stage 09 original/v2 report SHA-256 values remain
  `1bb8c7f9d1811ee0caceaaabbb65f146ee892e2f0e84bb88433fb5b844e5b520`
  and `8ab632b54e36c22ee7bc89212e53904092dba3cfa6e8fc0bc29a7285b4760db3`;
  final QA `FAIL` cites live-config replay and numeric seed-directory alias.
- Stage 10 M8 CPU/offline evidence passed; its candidate was not publicly
  released. PR #18 preserved the DEC-070 `STOP` closeout without tree drift.
- Stage 11 contract/result drafts are documentation only. Program Integrator
  read-only audit found a premature Stage 11 envelope choice and stale
  Stage 09/opening references. QA's first and delta reviews were conditional;
  the PI-authorized final review returned independent `PASS` on `0effe407`.
- PR #20 merged the Stage 11 documents at `4aed192`; GitHub Actions `tests`
  passed on `0effe407`, including the repository's existing synthetic CPU smoke.
  Stage 09 tracked files remain unchanged. CI also passed on the QA-reporting
  commit `ffc0bdf`. Merge is an integration fact, not a Stage 12 data gate.
- The proposed Stage 12 Charter received document-only independent QA `PASS`
  after clarifying that target-test class coverage needs approved metadata or
  a separate blinded metadata audit; otherwise admission stays `HOLD`. No data
  or ignored report bytes were opened. PR #21 carried the proposal and merged
  into `main` at `f83f894`; later Stage 12 audit QA is recorded separately.
- PR #21 CI `tests` passed on `d729d8c` (existing governance, pytest and
  isolated synthetic CPU smoke); this is proposal engineering evidence only.
  DEC-075/076 are PI authority records, not adequacy or model results.
- Added local `data/` contains canonical Stage 06 r2 manifest (SHA `44bafe...`),
  three matching official archives and 98/98 hash-matched approved train/val
  arrays. Original entities: Appliances 1, Beijing 12, Bike 1; Bike 71 train
  fragments are not independent sources. Seen channel counts 11/26 exceed
  Bike's 4, preventing its current paired H-01 count view. H-04 remains HOLD;
  no score or sealed array was opened.
- RK-56/57 track sparse Bike coverage and a Windows CRLF worktree registry-hash
  preflight risk; the canonical tracked Stage 06 registry bytes are unchanged.
- RK-58 tracks conflicting Bike `temp` normalization formulas in its bundled
  README versus the current UCI page; physical-unit semantics remain unverified.
- Independent Stage 12 audit QA returned `PASS` on the bounded packet after
  marking Bike `temp` semantics `conflict`; no source or Stage 13 gate is implied.
- PR #22 merged the audit packet at `392b785` after PR #21 integration. Its
  two CI pytest runs passed; DEC-078/079 record PI scientific decisions.
- Stage 13 Charter has document-only QA `PASS`, PI `GO` DEC-082 and two CI
  `pytest` passes; Draft PR #23 remains open and unmerged.

## Next action

Seek PI decision on the Charter's bounded metadata-only candidate search.
Named-source access/admission remains separate. Keep Electricity/test sealed
and DEC-070 release `STOP`.
