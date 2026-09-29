# FlyTS Current Research State

Updated: 2026-09-29

## Current stage

Stage 08 is closed with independent QA `PASS` and is merged at `9f41e0f`.
Stage 09 is closed at `HOLD`; DEC-057 independent QA remains `FAIL`, and the
PI-authorized PR #15 was merged into GitHub `main` at
`af46eb6058c4abc13535c063295431a94dca640e`. The merge tree
`077a555156384b4ec7562dcaa321c1ec9d4ed7a2` equals the reviewed Stage 09 head
tree. No numerical freeze, formal training, final-held-out opening or formal
analysis occurred. Stage 10 M0 is recorded, and DEC-061 gives Charter `GO` for
M2 through independent release QA. DEC-063 resolves the M7 decision gate by
selecting MIT and preserving but archive-excluding two historical personal-path
files. M7 and M8 passed for the pre-integration candidate. The first M9 review of
`d6e44f7` failed under DEC-064; remediation commit `d4407e8` fixed all four
findings and DEC-065 records the independent delta `PASS`. M2–M9 are complete.
DEC-066 records PI M10A `GO`; M10B remains closed.

## Current goal

Deliver the reviewed Stage 10 branch through push and a Draft PR under M10A,
then await user review/merge. Do not merge, tag or create a prerelease; M10B is
a separate post-merge PI decision.

## Canonical references

- `docs/research/stages/stage-10/CHARTER.md`
- `docs/research/stages/stage-10/M8_REPRODUCIBILITY.md`
- `docs/research/stages/stage-09/RESULT.md`
- `docs/research/stages/stage-09/QA_REPORT.md`
- `docs/DEVELOPMENT_PLAN.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/PROJECT_CONSENSUS.md`
- `docs/research/HYPOTHESES.md`
- `docs/research/REQUIREMENTS_TRACEABILITY.md`
- `docs/research/RISK_REGISTER.md`

## Confirmed decisions

- The user remains the final `GO`, `REVISE`, `HOLD` or `STOP` authority.
- Stage 10 targets `FlyTS-Mini v0.1 Research Preview`, an engineering/research
  preview rather than a validated model or scientific completion claim.
- Python package `flyts 0.2.0` and research artifact `v0.1` remain separate
  version axes. No package downgrade or PyPI publication is planned.
- No pretrained checkpoint is included. Stage 8 pilot artifacts cannot be
  promoted to selected, validated or optimal models.
- The prospective release code may remove the Stage 09 reporter's live-config
  dependency and reject numeric seed aliases. It cannot change Stage 09 reports,
  hashes, `HOLD` status or QA `FAIL`.
- The candidate release identity is tag `flyts-mini-v0.1-preview.1` with a GitHub
  prerelease, subject to a final PI release `GO` after integration and QA.
- The reproducibility package includes source, wheel/sdist, exact supported
  configs, documents, manifest/checksums, a synthetic fixture and offline verify
  instructions. It excludes raw data, outputs, checkpoints, embeddings, HARTH
  artifacts, Electricity model outputs and an unspecified wheelhouse.
- H-01 through H-03 have no formal result. H-04 is `not tested`; topology,
  robustness, foundation quality, transfer, CUDA and semiconductor claims remain
  unverified.
- Appliances and Beijing remain pretrain, Bike development-only and Electricity
  final-held-out. No dataset role, split, metric or scientific acceptance rule
  changes in Stage 10.
- Stage 10 uses at most three specialists, at most two concurrently, after Charter
  approval. The Research Director works alone through the Charter gate.
- DEC-061 approves the Stage 10 Charter and M2 through independent release QA.
  M10A push/Draft PR and M10B tag/prerelease remain pending.
- DEC-063 selects MIT and immutable historical-file treatment: the affected
  Stage 0/8 files stay byte-identical in Git but are excluded from new release
  archives by both `export-ignore` and the curated builder.
- DEC-064 preserves the first M9 `FAIL` and authorizes only the Charter-defined
  fixes for archive path validation, the generated fixture, QA manifest binding
  and stale M8 wording, followed by one independent recheck.
- DEC-065 records independent remediation `PASS`; it completes M9 evidence but
  does not authorize push, Draft PR, merge, tag or prerelease.
- DEC-066 grants M10A `GO` for branch push and Draft PR only. Merge, tag,
  prerelease, PyPI/checkpoint publication and future research remain unauthorized.

## Open questions

- Whether the user merges the Draft PR after review; M10B remains separate.

## Active risks

- A Research Preview could be mistaken for a validated foundation or production
  model despite the absence of a checkpoint and formal/final evidence.
- Reporter hardening could accidentally mutate or appear to supersede historical
  Stage 09 evidence and QA `FAIL`.
- Package `0.2.0` and research artifact `v0.1` could be conflated without explicit
  dual-version metadata and artifact hashes.
- Release archives could capture raw/ignored artifacts, credentials, absolute
  paths, user/company information or rights-unclear data.
- A dependency wheelhouse without an exact target OS/Python/PyTorch/device contract
  would overstate offline portability.
- Final-held-out/test access, new training or post-result numerical selection would
  reopen scientific work and invalidate the release-only scope.
- CUDA hardware remains unavailable; CPU evidence cannot create a CUDA claim.
- Existing Stage 09 risks concerning pseudo-replication, graph-cache drift,
  incomplete sufficient statistics and mutable replay inputs remain historical.
- Historical personal-path files remain in Git history. DEC-063 controls new
  archive redistribution but does not erase already-published history.
- The first M9 review found that malformed external package input could use a
  Windows drive-absolute member, the promised corpus fixture was absent, and the
  manifest could not bind a final QA verdict. DEC-065 controls those defects;
  future changed trees still require the same audit and M10A remains gated.

## Latest evidence

- GitHub PR #15 is merged at `af46eb6058c4abc13535c063295431a94dca640e`;
  its tree `077a5551…9d4ed7a2` equals reviewed Stage 09 head `a02a9935`.
- Stage 09 final reporter QA remains `FAIL`: `REPORT-v2` reads a live evaluation
  config and accepts a numeric directory alias such as `runs/07`.
- Stage 09 preserved original/v2 report hashes remain
  `1bb8c7f9…e5b520` and `8ab632b5…60db3`.
- The protocol-v2 matrix remains an unfrozen 60-row proposal with SHA-256
  `f2a9019f…786cf7`; no formal run used it.
- Electricity final-held-out evidence remains unopened and HARTH remains unadmitted.
- Stage 08 provides one-seed operational evidence only: four core arms completed
  400 CPU steps/3,200 exposures with independent QA `PASS`.
- The current package version is `0.2.0`; its version history moved from `0.1.0`
  when the foundation encoder MVP was introduced.
- DEC-063 adds MIT and dual archive exclusion. M7 re-audit passes: the commit-bound
  source, wheel, sdist and offline bundle contain no detected private path/name,
  secret, raw/checkpoint/embedding or traversal member; both historical files
  remain byte-identical in Git and absent from release archives.
- Candidate `14f95c9906bb771783686072d7cd0553094cc491` / tree
  `f2a50014f3d9870a9e88ed2554e1d8f40d84fd4c` is byte-stable across two builds.
  The external manifest SHA-256 is `bce6a87c…1cc5ecf`.
- M8 passes: final full suite `160 passed, 4 skipped` in 210.72 s; wheel/sdist
  no-index installs and `pip check` pass; installed-wheel CPU smoke, exact model
  resume, embedding export, prospective replay and bundle verification pass.
  Three skips report unavailable CUDA hardware and one reports Windows symlink
  creation unavailable; no CUDA support claim is made.
- First M9 verdict is `FAIL` on `d6e44f7`. The reviewed candidate itself was
  byte-stable and contained no detected unsafe member or private content, but the
  prospective input validator and bundle/manifest contract were incomplete.
- Remediation `d4407e800eb3ff54f205726626cee51aeed1e467` / tree
  `0c18e766e6d9a5666d6b28444b52d14e79f1b168` rejects portable absolute/traversal
  members, includes and verifies a 12-record generated fixture, and binds the QA
  report/verdict. Two candidates were byte-identical; full/focused tests, package
  installs, archive checks and Stage 09 immutability passed independent recheck.

## Next action

Push the M10A-authorized branch, open a Draft PR and stop for user review/merge.
After merge, reverify the exact merged tree and final assets before presenting
the separate M10B release gate.
