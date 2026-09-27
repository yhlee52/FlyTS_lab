# Stage 06 Independent QA Report

Date: 2026-09-27

Final verdict: **PASS**

Scope: approved public corpus v1 expansion only

## Verdict history

Initial QA was **FAIL**. It found that conversion silently omitted four short Bike
gap records totaling 41 non-purged source rows, and that a finite Python value such
as `1e100` became `inf` only after float32 assignment. It also found that the report
omitted actual purge durations and that the legacy 32-point documentation was not
clearly separated from Stage 06's 512-point contract.

Remediation retains every nonempty gap record, verifies contiguous source-index
coverage outside the two purges, rejects nonfinite float32 conversions, reports the
actual purge duration, and distinguishes the legacy and Stage 06 contracts. The one
allowed QA follow-up independently reproduced these fixes and issued **PASS**.

## Independent evidence

- Focused Stage 06 tests: 8 passed.
- Full suite: 84 passed, 3 CUDA hardware skips.
- Frozen r2 manifest SHA-256:
  `44bafe48196a4afd096e387dc672cad128d390ab7e5b413ea6cbeadf5f3e7f6c`.
- Registry SHA-256:
  `0095d4cd76ad5fdaeefeccdbb4322187892cc155bfac619ca4c8618ea50b9b20`.
- Full verification passed for 120 records: 85 train, 15 validation, 20 test.
- All 15 entities have contiguous retained source coverage outside the fixed purges.
  Bike now retains all 12,165 train rows, including the four short gap records.
- The overflow fixture raises `Electricity nonfinite value` after float32 conversion.
- Official Electricity was independently streamed and compared: `140256×370`, 900
  seconds, all 139,232 retained rows equal the float32 source values and are finite.
- All four archive hashes and selected-member hashes match configuration and report.
- Report `--check`, governance/notebook validators and `git diff --check` passed.
- The r2 smoke hashes match its manifest, registry and single checkpoint; all five
  dataset/mixed cases contain only approved coordinates, shapes, finite flags and
  memory fields.

## Limitations and remaining risks

- CUDA remains unavailable and unverified.
- No loss, model score, ranking, final-held-out performance or scientific comparison
  was inspected. Smoke success is not evidence of foundation quality or channel-count
  generalization.
- UCI rights statements and local notices are provenance evidence, not legal advice.
- Source coverage verification relies on the manifest's hash-bound `source_length`;
  pinned archive/member hashes bind that metadata to the admitted bytes.
- Short records are retained in the corpus but remain ineligible for model windows
  below the configured minimum context.
