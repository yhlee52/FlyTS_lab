# Stage 10 Independent QA Report

Verdict: **PASS**

Date: 2026-09-29

Reviewed source commit: `d6e44f711d84b25274ff45527c5d900357665bca`

The first M9 verdict was `FAIL`. Its evidence and blockers are preserved below;
the top-level verdict reflects the independently verified remediation recheck.
That first M9 `PASS` did not authorize M10A or M10B.

## Scope checked

- Stage 10 Charter, M7/M8 records, model card, release notes and evidence matrix.
- Stage 09 original/v2 evidence identities and final QA status.
- Head-bound M9 source, wheel, sdist, offline bundle, manifest and checksums.
- Package install, `pip check`, installed CLI help, reporter and release tests.
- Archive paths, checkpoint/data exclusions, personal paths and common secret
  signatures.

## Evidence

- Head-bound candidate verification and an independent replay build passed and
  were byte-identical.
- Focused reporter/release tests passed with one Windows symlink skip. M8 records
  the full suite as `160 passed, 4 skipped`.
- Separate no-index wheel and sdist installs, `pip check`, installed-package
  import and CLI help passed with the approved compatible CPU dependencies.
- Stage 09 report hashes remain
  `1bb8c7f9d1811ee0caceaaabbb65f146ee892e2f0e84bb88433fb5b844e5b520`
  and `8ab632b54e36c22ee7bc89212e53904092dba3cfa6e8fc0bc29a7285b4760db3`;
  Stage 09 remains `HOLD` with final QA `FAIL`.
- The two immutable historical personal-path files match their baseline blobs
  and are absent from candidate archives.

## Blockers

1. `_safe_member("C:/private.txt")` accepted a Windows drive-absolute package
   member, violating the fail-closed archive contract.
2. The offline bundle contained a generator but no generated corpus fixture and
   corpus manifest promised by the Charter.
3. The release manifest hardcoded independent QA as pending and had no supported
   mechanism to bind the final verdict and report provenance.

## Missing verification

- The closeout report stated that M8 was pending although the M8 record was
  already `PASS`.
- CUDA remains unavailable and `not tested`; the three CUDA skips and one
  Windows symlink skip are accurately disclosed.

## Required remediation and recheck

- Reject drive/root-absolute and traversal archive members with adversarial tests.
- Include and hash-verify an explicit generated synthetic corpus fixture.
- Derive the independent QA verdict and QA report hash from the source commit.
- Correct the stale M8 wording.
- Rebuild and reseal candidates, rerun focused/full checks as appropriate, and
  obtain an independent delta review before M10A.

## Recheck

Date: 2026-09-29. Reviewed remediation commit
`d4407e800eb3ff54f205726626cee51aeed1e467`, tree
`0c18e766e6d9a5666d6b28444b52d14e79f1b168`.

Recheck verdict: **PASS** for the four defects in the preserved first M9 `FAIL`.
Windows drive/root/traversal archive names are rejected; the offline ZIP contains
a hash-verified 12-record synthetic corpus and passes installed `flyts verify`;
the manifest derives the QA verdict and report SHA-256 from its source commit;
M8 wording is current. Full pytest, focused tests, candidate verification, byte
replay, no-index wheel/sdist installs, `pip check`, archive/privacy checks and
Stage 09 immutability checks passed. CUDA remains untested. At that recheck,
M10A/M10B remained pending PI gates.

## Post-merge closeout recheck

Date: 2026-09-29. Reviewed
`703e4a1dd0aff3edf8525f3fbe2869e3db1d26f9`, tree
`973a858e28b472f4a636ee6b28490fdf8c9149b5`, and its head-bound candidate.
Verdict: **FAIL** for documentation accuracy. PR #16 merge
`b193d91198adf8f7c5e5b1d7e177783252b7d932` has tree
`1f590601b977b5fb9d6cc9d219a0e8478ec4a4d5`, equal to reviewed head
`cb1a4b67be266438ae9565f5f10240cbc7397519`. The closeout diff is
documentation-only. The release report still calls M10A pending and instructs
obtaining its already completed push/PR gate; the Development Plan still says
push/PR remain gated. Correct those present-tense statements and rebind/reverify
the candidate before closeout.

Governance validation, full and focused pytest, release seal/verify, Python 3.12
byte replay, no-index wheel/sdist installs, `pip check`/CLI, 12-record offline
fixture, archive exclusion/privacy scan, and Stage 09 preserved report hashes
passed. CUDA remains not tested. Python 3.14 yields different gzip bytes despite
equal tar payloads; replay identity is evidenced on Python 3.12.

### Remediation recheck

Date: 2026-09-29. Reviewed documentation remediation commit
`c9f71d4acd9ecc0e62c45a973f30a6b24347f229`, tree
`94f78ecaeea3ad3438292f12e236cca4eac92fd8`. Verdict: **PASS** for the stale
M10A gate wording in the preserved post-merge `FAIL`. The release report and
Development Plan now state that PR #16 merged and that documentation closeout
and M10B remain pending. The change is documentation-only. Governance/notebook
validation, focused release/reporter tests, head-bound candidate seal/verify, a
byte-identical CPython 3.12 replay of all six assets, the 12-record offline
fixture, and archive/privacy checks passed. The prior full suite and no-index
package-install evidence remain applicable because no source, config, or tests
changed. Stage 09 report hashes and `HOLD`/QA `FAIL` remain preserved; CUDA is
not tested. Cross-Python gzip byte identity is explicitly unclaimed. This
recheck does not authorize a tag, prerelease, PyPI upload, checkpoint
publication, or M10B.
