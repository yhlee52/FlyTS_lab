# Stage 09A QA Report

Current verdict: **FAIL — DEC-056 final reporter remediation; Stage 09 HOLD**

The reporter's current arithmetic and byte replay are correct, but independent QA
found two fail-closed/provenance defects. Under the PI's final-cycle stop rule no
further remediation is proposed. Earlier bounded verdicts remain historical below.

## DEC-057 final remediation findings

- Original `REPORT.json` remains unchanged at SHA-256
  `1bb8c7f9d1811ee0caceaaabbb65f146ee892e2f0e84bb88433fb5b844e5b520`;
  `REPORT-v2.json` is
  `8ab632b54e36c22ee7bc89212e53904092dba3cfa6e8fc0bc29a7285b4760db3`.
- The six facts/raw hashes, 128 zero-dropout pairs per seed, record-first
  calculations and reported clean contrasts independently match. V2 remains
  `HOLD`, `exact_rules=null`, `claim=not tested`.
- V2 is not derived solely from the approved preserved report/facts/records: it
  reads the live evaluation config for `relative_floor` and its hash. Removing
  that live path makes replay fail despite all approved inputs remaining intact.
- Exact run-directory checking converts names to integers, so an extra `runs/07`
  alias is not rejected alongside `7/17/29`.
- Focused calibration tests report 12 passed; combined Stage 09 tests report 40
  passed. Governance, notebook and diff checks pass, but do not cover the two
  adversarial defects above.
- QA did not rerun training/evaluation or access Electricity, HARTH or final data.

## DEC-057 gate recommendation

`FAIL` the reporter remediation and place Stage 09 at `HOLD`. One Bike record,
synthetic count views, inconsistent H-02 signs and reporter protocol defects do
not justify an M2 numerical freeze. Per DEC-056, stop remediation and request PI
closure disposition; at that gate M2, M5/M6, final access, claims, PR and Stage 10
remained closed.

The PI accepted this `HOLD` closure under DEC-058 and authorized a Draft PR of
the preserved package. This does not change the QA verdict or open a later gate.

## DEC-052 protocol-v2 consistency findings

- Independent parsing found 60 unique rows: 15 each for `fly_like`,
  `degree_preserving_rewired`, `random_sparse` and `temporal_only`.
- The matrix SHA-256 is
  `f2a9019f093072e44e68b4f6dd8bab9abfe1655dd4b6ed94719ae54246786cf7`.
- Validators enforce the exact training/topology/control seeds, CPU float32,
  10,000 steps, 80,000 exposures, pairing and provenance contracts. Stage 09
  formal `run_config` rejects GRU, and active metadata rejects H-04.
- Charter, protocol, plan, hypothesis trace and result records consistently limit
  active inference to H-01–H-03. H-04/HARTH remain `HOLD`/`not tested`; Stage 08
  GRU evidence and both HARTH audit artifact hashes remain unchanged.
- Focused matrix/rehearsal/resume tests report 4 passed; the full Stage 09 file
  reports 28 passed. Governance validation, notebook validation and
  `git diff --check` pass; only line-ending warnings were emitted.
- QA did not admit data, run training, access final assets or edit tracked files.

## DEC-052 gate recommendation

Accept `PASS` for protocol-v2 proposal consistency only. Continue Stage 09A at
`HOLD` until development-only H-01–H-03 calibration justifies exact M2 numerical
rules and the PI separately freezes them. M5/M6, final opening, claims, PR and
Stage 10 remain closed.

## DEC-049 scanner evidence findings

- Metadata-only replay produced byte-identical corrected artifact SHA-256
  `493cd08c3366cc311c9a1ef297e26c79415cb466f591795dd063af136fa56fe0`.
  The prior failed artifact remains unchanged at
  `23ab3d6bb87d1275ba2040873ab81d7d7769a13f2e5b339ff8be97543bd99294`.
- The scanner now requires exact official codes
  `1/2/3/4/5/6/7/8/13/14/130/140` independently in train, validation and test;
  an arbitrary set of 12 labels remains `HOLD`.
- Subject-local cadence now drives gap and segment evidence. `S006` records a
  10 ms mode, 38 gaps and 461 contiguous segments; the archive-wide mode remains
  20 ms, but `cadence_mismatch=true` and the PI cadence decision is retained.
- Namespace `flyts-stage09-harth-candidate-v1`, seed `1`, and the exact 14/4/4
  split are unchanged. Test still lacks official code `14`, so status is `HOLD`.
- Focused HARTH tests: 13 passed. Full Stage 09 file: 28 passed. CLI overwrite
  rejection preserves existing output bytes.
- No official signal values, arrays, windows, probes, training results, alternate
  split or final assets were accessed.

## DEC-049 gate recommendation

Accept the bounded scanner repair and QA `PASS`. Keep HARTH scientific admission
and Stage 09A on `HOLD`; the class-coverage, cadence-interpretation and notice
conditions require a separate PI disposition. This QA does not open M2 or any
later gate.

## Preserved DEC-047 failed scanner review

## DEC-047 HARTH admission findings

- The official ZIP is 310,795,012 bytes with SHA-256
  `2ab54d6b11467ddbe998dfb60355f9f1ae181b0af7a89e7c78bb7af2cf16b64a`.
- Exact replay with namespace `flyts-stage09-harth-candidate-v1` and seed `1`
  reproduced ignored artifact SHA-256
  `23ab3d6bb87d1275ba2040873ab81d7d7769a13f2e5b339ff8be97543bd99294`.
- The deterministic split is disjoint 14/4/4. Train and validation contain the
  official 12 codes; test lacks code `14`. No alternative split was searched.
- `S015` and `S021` contain strictly increasing integer source indexes with 36
  and 41 gaps; `S023` contains a contiguous unnamed row ordinal. These variants
  are metadata and are not six-channel inputs.
- The scanner incorrectly uses the archive-wide 20 ms mode for every subject.
  `S006` actually has 408,670 regular 10 ms intervals and 38 local gaps, but the
  artifact reports 408,708 gaps and 408,709 segments. Independent metadata-only
  reconstruction gives 461 segments. The artifact consequently omits the
  required cadence PI decision.
- The scanner accepts any 12 shared labels rather than the official registered
  set `1/2/3/4/5/6/7/8/13/14/130/140`.
- HARTH-only metadata tests pass (11), but they encode both defects above and do
  not make the admission evidence valid.

## DEC-047 gate recommendation

Keep HARTH admission and Stage 09A at `HOLD`. Do not repair the split by seed
search or revise the class metric after seeing coverage. Correct scanner evidence
only under a new authorized remediation; any split/class-policy change requires
a separate PI protocol decision. No signal values, arrays, windows, probes,
training results or final-held-out evidence were inspected by QA.

## Preserved bounded M4 tooling verdict

Verdict: **PASS — bounded M4 tooling review**

Date: 2026-09-28

This is the replacement M4 verdict after DEC-041 and DEC-043 remediation. It
accepts the blind tooling/rehearsal scope only. HARTH admission, numerical freeze,
M5/M6 and final access retain their separate gates.

## Accepted evidence

- Registry v2 rejects sealed HARTH test paths before access, enforces the exact
  six input signals, separates labels and rejects cross-split subjects.
- Graph-cache hits reconstruct a validated artifact without generator execution;
  generated and loaded buffers match and corruption/config drift reject.
- At the time of that review, the historical proposal contained all 65 then-
  registered rows and the H-02 temporal-only control changed only channel
  masking/dropout. DEC-051 supersedes that active matrix with 60 rows.
- The atomic unseal ledger binds sessions, UTC events and input/output hashes and
  rejects stale locks, invalid transitions and reruns.
- A cache-consuming one-row synthetic rehearsal ran two trainer subprocess phases,
  preserved its pre-resume checkpoint, derived 2 steps, 4 exposures and 2,348
  parameters from artifacts, selected the earliest minimum and replayed the locked
  report byte-for-byte. Overwrite, cache miss and tampering reject.
- H-03 validates the exact nested cells/rules and rejects nonnumeric, nonfinite and
  missing inputs before sampling. It checks every paired difference, inner/outer
  accumulation and mean, stored/sorted resample and selected bound before support.

## DEC-043 adversarial checks

- The exact finite-input overflow fixture (`fly_like=0`, both controls `1e308` in
  all 15 cells) raises `H03 protocol failure` before support.
- Opposite-sign finite inputs that overflow a paired difference also raise.
- The finite `1e306` fixture retains the expected `-1e306` upper bound.
- A varying-loss fixture confirmed shared draws across both contrasts; the random
  upper bound was exactly twice the rewired bound and the conjunctive IUT failed
  when only the random contrast failed.

## Verification

- H-03 focused suite: 8 passed.
- Stage 09, Stage 06 corpus and topology-control regressions: exit `0`.
- Full suite after the micro-remediation: exit `0`, three skips.
- Ignored rehearsal: `outputs/stage09/dec041-rehearsal/`; independent replay passed.
- No tracked files were changed by QA and no final-held-out/test data was opened.

## Preserved limitations and gates

- The rehearsal sufficient-statistic file is explicitly synthetic and wraps an
  aggregate validation loss with `target_count=1`; it is not proof of formal
  per-record target-sum/count capture. Actual formal evidence must persist those
  statistics directly from evaluator outputs.
- HARTH remains unadmitted because of the absent bundled notice, 10 ms observed
  cadence versus 50 Hz metadata and three extra-column CSV headers.
- Numerical guards/effects/uncertainty rules remain unfrozen. Passing M4 QA does
  not authorize M5 immutable freeze, M6 formal training or final opening.

## Gate recommendation

Accept M4 QA for the bounded tooling package. Keep Stage 09A on `HOLD` until the
PI resolves HARTH admission and the exact M2 numerical freeze packet.
