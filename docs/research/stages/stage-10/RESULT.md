# Stage 10 Result — FlyTS-Mini v0.1 Research Preview

Status: **engineering closeout merged; M10B STOP — not publicly released**

Date: 2026-09-30

## Outcome

Stage 10 completed the approved engineering release/closeout scope. FlyTS now has
a deterministic, checkpoint-free Research Preview candidate with source,
`flyts 0.2.0` wheel/sdist, exact supported configs, documents, classified
manifest/checksums and an offline CPU path containing an explicit generated
synthetic corpus fixture.

This is not scientific/model completion. Stage 09 remains `HOLD` with final QA
`FAIL`; H-01–H-03 have no formal result and H-04 is `not tested`. No final-held-out,
transfer, pretrained-checkpoint, CUDA or semiconductor result is claimed.

## Milestone status

| Milestone | Result |
|---|---|
| M0–M1 baseline/Charter | `PASS`; PI Charter `GO` recorded |
| M2 inventory | `PASS`; release class, evidence tier and QA status remain distinct |
| M3 prospective hardening | `PASS`; declared inputs only, canonical seeds, fail-closed replay |
| M4 closeout documents | `PASS`; claim/checkpoint/hardware boundaries explicit |
| M5 manifest/checksums | `PASS`; deterministic commit/tree/file/artifact identities |
| M6 distribution candidates | `PASS`; source, wheel/sdist and offline bundle verify |
| M7 security/rights | `PASS`; MIT, exclusions, portable-path and archive controls |
| M8 clean room | `PASS`; CPU install/smoke/resume/embed/replay/no-network evidence |
| M9 independent QA | initial `FAIL` preserved; DEC-064 remediation recheck `PASS` |
| M10A/M10B | PR #16 and PR #17 merged without tree drift; M10B `STOP`; no public release |

## Independent QA history

The first M9 review of `d6e44f7` found four release-hardening defects and returned
`FAIL`. Remediation commit `d4407e800eb3ff54f205726626cee51aeed1e467`, tree
`0c18e766e6d9a5666d6b28444b52d14e79f1b168`, fixed all four. Independent delta
QA repeated full/focused tests, package installation, `pip check`, fixture and
candidate verification, deterministic replay, privacy/archive checks and Stage 09
identity checks and returned `PASS`. The original failure remains visible in
`QA_REPORT.md`.

## Distribution boundary

Included assets are the full curated source archive, `flyts 0.2.0` wheel/sdist,
offline ZIP, external manifest and `SHA256SUMS`. The ZIP contains 12 generated
seed-7 records plus their corpus manifest/checksum, but no dependency wheelhouse.

Excluded are raw public/company data, Stage 08/09 raw outputs, every checkpoint
and embedding, HARTH artifacts, Electricity model outputs, target-unspecified
dependencies and unverified CUDA/formal/transfer outputs. Two immutable historical
personal-path evidence files remain in Git history but are excluded from new
source/offline archives.

## Gate boundary

DEC-066 M10A `GO` authorizes only push and creation of a Draft PR. The user
performed the merge as `b193d91198adf8f7c5e5b1d7e177783252b7d932`.
Its tree `1f590601b977b5fb9d6cc9d219a0e8478ec4a4d5` exactly equals reviewed head
`cb1a4b67be266438ae9565f5f10240cbc7397519`; integration introduced no drift.
DEC-067 authorized the documentation-only closeout and additional independent QA.
PR #17 merged as `27f81eb2607444739a90b32a94ef11f184687a93`; its tree
`3d80b52d33eeeb6a84eb1289f72a39584f2da280` equals reviewed head `1f2fdec`.
DEC-070 sets M10B to `STOP`: no tag, GitHub release/prerelease, PyPI upload or
checkpoint publication. No final public-release asset set was produced.
