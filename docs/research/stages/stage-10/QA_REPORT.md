# Stage 10 Independent QA Report

Verdict: **FAIL**

Date: 2026-09-29

Reviewed source commit: `d6e44f711d84b25274ff45527c5d900357665bca`

This is the preserved first M9 verdict. M10A remains `HOLD` until the defects
below are remediated and the independently reviewed remediation result is added
to this report. A later recheck does not erase this finding.

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

Pending.
