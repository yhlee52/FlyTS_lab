# FlyTS Current Research State

Updated: 2026-09-28

## Current stage

Stage 08 is closed and PR #14 is merged into GitHub `main` at `9f41e0f`; the merge
tree matches the reviewed Stage 08 head. Stage 09A bounded tooling has replacement
M4 QA `PASS` and PI acceptance under DEC-045. The DEC-046 HARTH admission pass
ended in coverage `HOLD`; DEC-048 corrected its scanner defects and DEC-049 QA
reports `PASS` for scanner evidence only. The PI accepted HARTH admission `HOLD`
under DEC-050 and approved protocol v2 under DEC-051: H-01–H-03 only, with an
unfrozen 60-run proposal. DEC-052 independent v2 consistency QA reports `PASS`.
DEC-054/055 completed the bounded six-run package with a locked `HOLD` report.
DEC-057 final remediation QA is `FAIL`. Under DEC-058 the PI accepted Stage 09
closure at `HOLD` and authorized a Draft PR of the preserved package.

## Current goal

Review Draft PR #15 and its checks. Do not start another repair, rerun,
threshold-selection, merge or Stage 10 cycle without a new PI gate.

## Canonical references

- `docs/research/stages/stage-09/CHARTER.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/PROJECT_CONSENSUS.md`
- `docs/DATASETS.md`
- `docs/TOPOLOGY_CONTROLS.md`
- `docs/research/HYPOTHESES.md`
- `docs/research/REQUIREMENTS_TRACEABILITY.md`
- `docs/research/RISK_REGISTER.md`

## Confirmed decisions

- The user remains the final `GO`, `REVISE`, `HOLD` or `STOP` authority.
- Stage 9 uses a 9A readiness/freeze gate followed by a separately approved 9B
  formal execution; final opening has another mandatory PI gate.
- Appliances and Beijing remain pretrain, Bike development-only and Electricity
  final-held-out. Existing role assignments cannot change.
- HARTH is the proposed encoder-excluded target-local classification dataset. Its
  official bytes, notices, labels, subjects and deterministic 14/4/4 split require
  Stage 9A admission before use; its test split remains sealed.
- Proposed formal seeds are training `7/17/29/43/59`, topology `7/17/29` and
  controls `5007/5017/5029` under a crossed 3-by-5 design.
- Proposed formal compute is CPU float32/four threads, 10,000 steps and 80,000
  exposures per run. CUDA remains `미검증`.
- The protocol-v2 proposal has 60 runs: 45 topology runs and 15 temporal-only
  Fly masking controls. GRU/H-04 are excluded; dense-leaky remains diagnostic-only.
- H-03 requires both registered topology contrasts under a conjunctive IUT. Windows
  are not inferential units; Electricity is aggregated record-first.
- Graph caching is allowed only before results with exact buffer/hash equivalence.
- Exact numerical guards, practical-effect thresholds and uncertainty configuration
  remain pending. Insufficient calibration evidence is `HOLD`.
- The tracked 60-run matrix and cache/unseal interfaces are unfrozen proposals.
  DEC-045 accepts only the historical 65-row bounded M4 tooling result.
- DEC-046 authorized one metadata-only HARTH candidate, not admission. Namespace
  `flyts-stage09-harth-candidate-v1` and seed `1` were used once; no alternative
  may be tried after the observed coverage failure without a new PI protocol.
- DEC-049 accepts the corrected scanner evidence only. The exact split, class
  metric and HARTH admission status remain unchanged and unfrozen.
- DEC-050 accepts HARTH admission `HOLD` under the current protocol. H-04 cannot
  proceed with HARTH and remains `not tested` unless a new protocol is approved.
- DEC-051 approves protocol v2 scope and budget: H-01–H-03, 60 proposed runs,
  no GRU formal arm. M2 and all execution gates remain pending.
- DEC-052 accepts the 60-row protocol/config/tooling package as internally
  consistent. It does not justify numerical rules or authorize a later gate.
- DEC-053–056 record the bounded calibration/final repair. DEC-057 QA `FAIL`
  ends automatic remediation and recommends Stage 09 `HOLD` closure.
- DEC-058 accepts Stage 09 `HOLD` closure and authorizes a Draft PR only. It does
  not authorize merge, Stage 10, a later research gate or any scientific claim.

## Open questions

- Whether the PI later approves merging the preserved package or a revised
  Stage 10 scope. No Stage 10 work is currently authorized.

## Active risks

- Final-held-out/test access or Bike-driven formal selection invalidates later evidence.
- HARTH/H-04 or GRU could be accidentally reintroduced despite DEC-051 exclusions.
- Inferring a calibration budget or count threshold from sparse Bike evidence
  would make H-01/H-02 rules post hoc.
- Reporter v2 depends on a live evaluation config and accepts a numeric seed alias;
  DEC-057 stop rule leaves these defects unresolved under `HOLD`.
- Three graph clusters and one Electricity record may be insufficient for the
  proposed interval claims; pseudo-replication is prohibited.
- Cache/config drift can silently change topology; exact graph-buffer equivalence is required.
- H-03 derived-finiteness is guarded, but only synthetic statistical fixtures have
  been exercised; no formal endpoint evidence exists.
- Synthetic sufficient statistics preserve/replay artifacts but do not prove real
  per-record target-sum/count capture.
- Rewired setup dominates current CPU estimates; Stage 08 timings are descriptive only.
- In-place resume, incomplete sufficient statistics or mutable analysis bytes can
  break exact replay.

## Latest evidence

- PR #14 merged at `9f41e0f`; its tree equals reviewed head `3369ae9`.
- Stage 08 core arms each completed 400 steps/3,200 exposures on CPU with independent
  QA `PASS`; these values are operational/descriptive and cannot select Stage 09.
- Stage 06 manifest/registry hashes remain `44bafe48…e7f6c` and `0095d4cd…b9b20`;
  no final-held-out model result has been inspected.
- Stage 03 numerical guards, thresholds and uncertainty settings remain candidate;
  prior QA found the evidence insufficient for a freeze.
- The current environment is PyTorch 2.14.0+cpu. Hardware visibility does not create
  a CUDA claim or authorize CPU/GPU mixing.
- DEC-039 records Stage 9A implementation `GO` with five sequential specialist roles,
  at most two specialists active concurrently.
- Official HARTH archive SHA-256 is `2ab54d6b…16b64a`; it has no bundled notice.
- The sole 14/4/4 candidate has all 12 official labels in train/validation but
  only 11 in test, missing `14`. No alternate namespace or seed was searched.
- DEC-047 failed artifact SHA-256 `23ab3d6b…bd99294` is preserved. Corrected
  artifact SHA-256 `493cd08c…56fe0` replays exactly and records `S006` at 10 ms,
  38 gaps and 461 segments while test remains missing code `14`.
- The canonical protocol-v2 proposal has 60 unique rows: 15 each for fly-like,
  rewired, random and temporal-only. Matrix SHA-256 is `f2a9019f…786cf7`.
- Matrix validation rejects GRU, H-04 metadata, missing, duplicate or extra rows;
  focused matrix/rehearsal tests and all 28 Stage 09 tests pass locally.
- DEC-041 fixed input-level H-03 validation and added a cache-backed one-row
  two-process rehearsal with locked byte replay; no final data was opened.
- DEC-043 records the user's authorization for one final derived-finiteness patch
  and independent QA rerun; no broader remediation is authorized.
- DEC-043 QA reports `PASS`: exact `1e308` and opposite-sign overflows fail closed,
  safe finite and paired IUT fixtures remain correct, and full tests pass (3 skips).
- DEC-045 records the PI's `GO` accepting the bounded M4 tooling result; it leaves
  M1/M2 on `HOLD` and does not open M5, M6, final access, claims or PR work.
- DEC-046/047 record the bounded HARTH pass, the preregistered coverage stop and
  the M1 QA failure. No arrays, windows, probes, training or final data were used.
- DEC-048/049 record the scanner-only correction and independent QA `PASS`; the
  PASS does not change HARTH admission `HOLD` or authorize any later gate.
- DEC-050 records the PI's acceptance of HARTH `HOLD`; H-04 is not tested and no
  alternative split, metric or target is authorized.
- DEC-051 records the PI's H-01–H-03/60-run option A decision. Historical GRU and
  65-row QA evidence remain preserved but cannot support protocol-v2 readiness.
- DEC-052 independent QA reports `PASS` for v2 consistency: 60 unique rows, 15
  per arm, matrix SHA-256 `f2a9019f…86cf7`, 4 focused and 28 Stage 09 tests passed.
  Governance, notebook and diff checks also passed; no data or final asset opened.
- DEC-054–057 preserve original SHA `1bb8c7f9…e5b520` and v2 SHA
  `8ab632b5…60db3`. Arithmetic matches, but live-config and `07` alias defects
  produce final QA `FAIL`; no training/evaluation rerun or final access occurred.
- DEC-058 closes Stage 09 at `HOLD`; DEC-059 records Draft PR #15 at head
  `4f9cd75`. H-01–H-03 have no result and H-04 remains not tested.

## Next action

Review Draft PR #15 and wait for the next PI gate. Do not remediate, freeze rules,
begin M5/M6, open final data, merge the PR, start Stage 10 or expand any claim.
