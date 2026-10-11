# Stage 13 result — Protocol v3 and Compute Budget Freeze

Status: **closed at PI `HOLD` (DEC-099); independent document QA `PASS`;
protocol/budget not frozen; Stage 14 NO GO**. Date: 2026-10-11. The PI chose to
stop the current Stage 13 freeze attempt and asked for lower-burden recovery
paths. This is a valid infeasibility finding under the [Charter](CHARTER.md),
not a positive H-01–H-03 result or permission to change the Stage 11 contract.

## Evidence and decision basis

- Stage 12 admitted Appliances and Beijing only for existing pretrain uses,
  and Bike only for dimensionless development diagnostics (DEC-078/079).
  Training-seen channel counts are 11 and 26; Bike has four channels and
  one original entity. Its 71 train fragments, windows and repeated seeds
  cannot supply independent H-01 count evidence or a paired 11-channel
  same-record view. Beijing's 12 stations share place and time.
- Stage 13 official-document screens and bounded source audits are in the
  linked packets. The PhysioNet source/use gate remains `HOLD` under the
  PI's non-human, clearly reusable-data direction (DEC-092). The open-data
  screens did not admit another held-out source.
- Cubico Kelmarsh v4's owner-stated CC BY 4.0 record and six physical
  turbines made it a candidate, not an admitted source. Approved DEC-096/097
  reads verified two small metadata files and 60 mapping title pairs; the
  latter had independent provenance/claim QA `PASS` (DEC-098). The response
  bytes and hashes remain Director-reported, because QA did not replay
  source access. A mapping entry is not a concurrent usable channel.
  Kelmarsh's time coverage, per-turbine availability, independent-unit
  dependence, split and paired 11/26/>26 views remain unverified. Its two
  metadata access caps were exhausted at closeout. DEC-104 later read only
  the 2016 ZIP directory, with DEC-105 bounded QA `PASS`. DEC-107 then read
  one 8,192-byte prefix including compressed member bytes; the first line
  parsed as one comma-delimited field with header identity unverified.
  DEC-107 bounded result QA `PASS` did not replay the response. No full
  member, archive or model score was opened. Channel coverage remains HOLD.
- No labeled H-04 target was admitted. HAR/HARTH keep their prior `HOLD`
  reasons; H-04 is `not tested`. Q2/Q3 are unavailable. Electricity and
  every test signal/score remain sealed.

## Charter acceptance and missing freeze package

| Required item | Stage 13 outcome |
|---|---|
| Eligible held-out source with approved rights, role, split and independent paired count observations | **Unmet.** Kelmarsh is metadata-only and unadmitted; existing Bike cannot pair to seen count 11. |
| Registered H-01/H-02/H-03 endpoints, integer dropout, matched topology controls, uncertainty and selection rules | **Unmet.** No protocol v3 or statistical analysis plan was frozen. |
| Low/medium/high resource envelopes, exact environment, selected run matrix and compute `GO` | **Unmet.** No budget or formal run was authorized. |
| Versioned configuration, freeze manifest, hashes, synthetic adversarial preflight and independent pre-freeze QA `PASS` | **Unmet.** Source metadata scripts and their tests are not a frozen runner/reporter. |
| PI protocol/budget `GO` and Stage 14 handoff | **Not granted.** DEC-099 is a Stage 13 `HOLD`. |

The completed work is the Charter, bounded candidate screens and access
packets, approved metadata audits, their narrow independent QA records and
decision/provenance trail. PRs #23–34 later merged into `main` at `c87eaad`
under DEC-101; successful CI verifies code/document checks only.
The [closeout QA](QA_REPORT.md) passed the bounded `HOLD` packet under
DEC-100, not a protocol freeze.
No Stage 13 formal training, model evaluation, checkpoint, numerical
threshold, seed, experiment matrix, compute envelope or CUDA path exists.

## Gate and recovery

Stage 14 is defined as a preflight of the **frozen** runner, reporter,
matrix and approved budget. It cannot start from this `HOLD`. The
[recovery options](RECOVERY_OPTIONS.md) compare a narrow open-licensed
Kelmarsh availability audit, a new PI-approved narrower contract and an
early Phase 02 `HOLD`. The PI selected bounded Kelmarsh route A under DEC-102;
that choice does not approve source admission. Reopening Stage 13
requires its named data/scope gates, a complete v3 and budget packet,
independent pre-freeze QA `PASS` and an explicit PI protocol/budget `GO`.
Synthetic engineering checks under a separately approved scope would not
count as Stage 14 completion.

Stage 09's `HOLD`, final QA `FAIL` and report hashes are unchanged. DEC-070
public-release `STOP` remains. No Stage 13 PR merge is approved by DEC-099.

## Bounded recovery closeout (DEC-102–110)

The PI selected route A and separately approved the exact DEC-104 and DEC-107
reads. The directory inventory had bounded result QA `PASS`; the 2016
audit-only turbine-1 prefix had pre-read and bounded result QA `PASS`.
It produced **one first-line field under a comma parser**, with header identity
and delimiter unverified. The official owner record did not state the member
format; DEC-108's one-page screen received bounded independent QA `PASS` under
DEC-109. These QA verdicts check access/report limits, not eligibility or
model performance. The six turbines share one farm and 2016 is excluded from
formal roles. No independent held-out H-01 paired count observations were
established and no Kelmarsh source/role/split was admitted.

Under the PI's bounded autonomy delegation (DEC-110), the Director closes
this low-cost recovery at the existing Stage 13 **HOLD**. Protocol v3,
low/medium/high compute choices, pre-freeze QA and PI protocol/budget `GO`
remain absent. Stage 14 is **NO GO**. No further source access or external
outreach was performed. The PI later authorized PR #35's merge (DEC-111),
and it merged at `dab9ac5830c418da16aabf5b2418b97da41e5f9d`. This
integrates the bounded HOLD packet without satisfying the freeze gate.
