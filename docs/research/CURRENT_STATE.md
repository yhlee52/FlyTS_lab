# FlyTS Current Research State

Updated: 2026-10-11

## Current stage

Stage 08 closed with independent QA `PASS`. Stage 09 closed at PI-accepted
`HOLD` (DEC-058) with DEC-057 final reporter QA `FAIL`; its PR #15 merged without
changing the reviewed tree. No numerical freeze, formal training, formal/final
analysis or Electricity opening occurred. H-01–H-03 have no formal result; H-04
is `not tested`. Stage 10 engineering closeout merged through PR #18, but DEC-070
stopped M10B public release. PR #19 merged the proposed Phase 02 plan into
`main` at `52fd44af0145e19d5f26138382bb0661e975eb09`. DEC-071 approved its
objective; DEC-072 authorized Stage 11 document-only contract work. Stage 11
independent QA returned `PASS` after one PI-authorized extra review (DEC-073),
and the PI accepted the Stage 11 result under DEC-074.
The document-only Draft PR #20 is open from
`codex/stage-11-qualification-contract` (initial commit `b15b769`); it is not merged.

## Current goal

Prepare a proposed Stage 12 Charter from the accepted Stage 11 contract and
handoff. Stage 12 data access, source admission, role/split decisions and every
later research gate require separate PI approval. DEC-070 no-release boundary
remains in force; Draft PR #20 is not merged.

## Canonical references

- `docs/research/PHASE_02_FORMAL_VALIDATION_PLAN.md`
- `docs/research/stages/stage-11/CHARTER.md`
- `docs/research/stages/stage-11/RESULT.md`
- `docs/research/stages/stage-11/QA_REPORT.md`
- `docs/research/DECISION_LOG.md` (DEC-070–074)
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
  Stage 12 Charter drafting is authorized, data work and PR merge are not.

## Open questions

- Stage 12 Charter scope and its separate PI approval remain open. Stage 11
  result `GO` authorizes a Charter proposal only, not data work.
- Dataset suitability/admission, minimum coverage, statistical thresholds,
  seed/matrix, budget, H-04 target, CUDA environment and final open remain future
  decisions with the named stage gates.

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
- Draft PR #20 contains the Stage 11 documents; GitHub Actions `tests` passed on
  `0effe407`, including the repository's existing synthetic CPU smoke. Stage 09
  tracked files remain unchanged. CI also passed on the QA-reporting commit
  `ffc0bdf`; DEC-074 records PI acceptance without authorizing PR merge.

## Next action

Draft the Stage 12 Charter as a proposal against the accepted Stage 11 contract;
request separate PI `GO` before any Stage 12 data work. Keep Electricity/target
test sealed and do not merge Draft PR #20 without separate PI approval.
