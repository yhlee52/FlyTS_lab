# Stage 09A Readiness Record

Status: HOLD — PI accepted closure under DEC-058; Draft PR authorized

## M0 baseline

- Work started from GitHub `main` merge commit
  `9f41e0fcf55a8b1a606e21bb53c1220bdc57dfc3` on the focused branch
  `codex/stage-09-formal-study`.
- PR #14's merge tree matches the reviewed Stage 08 head tree. The Stage 08
  evidence bytes and QA conclusion were not changed.
- `DEC-039` is controlling: it authorizes M0--M4 only. Older protocol wording
  that could be read as automatic Stage 09 final access was reconciled with the
  separate formal-run and final-open gates.

## HARTH pre-admission audit

Facts from the official UCI metadata, checked without downloading the archive or
opening target-test arrays:

- 22 subject CSV files are described at 50 Hz.
- Timestamp, six triaxial accelerometer signals (`back_x/y/z`, `thigh_x/y/z`)
  and an activity label are described; the label is a target, never an input.
- The landing page states CC BY 4.0 and describes 12 activity codes.

The official archive was then downloaded to ignored storage solely for admission
audit. It is 310,795,012 bytes with SHA-256
`2ab54d6b11467ddbe998dfb60355f9f1ae181b0af7a89e7c78bb7af2cf16b64a`.
It contains 22 `harth/S###.csv` members and no bundled README, notice or license.
The first inspected timestamps are 10 ms apart, conflicting with the landing
page's 50 Hz description. Most headers match the documented eight columns, but
`S015` and `S021` add an `index` column and `S023` adds a leading unnamed column.
The strict audit stopped on this schema mismatch before selecting or approving a
subject split; it did not materialize arrays or run a target-test probe.

Admission is therefore `HOLD`. The cadence discrepancy, absent bundled notice
and extra source columns require an explicit interpretation before any converter
may discard/resample data. HARTH is not present in a frozen registry, and the
audit namespace/seed and subject assignment remain unfrozen.

## DEC-046 one-shot admission candidate

The approved metadata-only pass fixed one audit candidate before reading its
coverage: namespace `flyts-stage09-harth-candidate-v1`, seed `1`, canonical JSON
SHA-256 ranking and a single 14/4/4 slice. It produced train subjects
`019/015/024/018/020/012/016/006/026/010/014/008/028/009`, validation subjects
`027/017/025/021`, and test subjects `013/022/023/029`. Train and validation have
all official 12 label codes; test lacks code `14`. No alternate seed or namespace
was tried. This invokes the preregistered coverage stop condition and leaves the
candidate unfrozen and HARTH unadmitted.

The scalar audit found that `S006` alone predominantly uses 10 ms timestamps
(408,670 intervals and 38 local gaps), while the other subjects predominantly use
20 ms. `S015`/`S021` have validated increasing integer source indexes and `S023`
has a contiguous unnamed row ordinal; none is a signal input. The archive still
has no bundled notice.

Independent QA reported `FAIL` for the remediation artifact. The scanner uses the
archive-wide 20 ms mode for subject gap/segment calculations, hides the `S006`
cadence conflict, and checks only the number of shared labels rather than the
official code set. The ignored artifact is byte-replayable at SHA-256
`23ab3d6bb87d1275ba2040873ab81d7d7769a13f2e5b339ff8be97543bd99294`, but it is
invalid as admission evidence. No arrays, windows, probes or training were run.

## DEC-048/049 scanner correction

The PI authorized a scanner-only correction and independent rerun without changing
the namespace, seed, split or class metric. The corrected audit requires the exact
official code set independently in each split and computes cadence, gaps and
segments per subject. `S006` now records a 10 ms local mode, 38 gaps and 461
segments; the archive-wide mode remains 20 ms, while `cadence_mismatch=true` and
the PI cadence decision is explicit.

The corrected artifact is `outputs/stage09/harth-admission-candidate-dec048.json`
in ignored storage, SHA-256
`493cd08c3366cc311c9a1ef297e26c79415cb466f591795dd063af136fa56fe0`.
Independent QA reproduced it byte-for-byte and reports `PASS` for scanner evidence.
The prior artifact remains preserved. Scientific status remains `HOLD`: the same
test subjects still lack class `14`, the `S006` semantics conflict remains, and no
bundled notice exists. No alternate split, array, window, probe or training was run.

## DEC-050 PI disposition

The PI accepted HARTH admission `HOLD` under the existing protocol. The failed
split, old and corrected audit artifacts, and no-search history remain preserved.
HARTH cannot enter registry v2 or H-04; H-04 is `not tested` unless a separately
approved protocol version changes the target or Stage 09 scope. This disposition
does not authorize M2 or any later gate.

## DEC-051 protocol-v2 scope

The active proposal now covers H-01–H-03 only. Its 60 rows are 45 crossed
topology runs and 15 paired temporal-only controls; GRU is excluded from Stage 09
formal scope. H-04/HARTH remain historical `HOLD`/not-tested evidence. The
historical 65-row M4 QA does not accept the revised bytes. DEC-052 fresh v2 QA
independently accepts the 60-row proposal consistency, but not numerical freeze.

## DEC-052 protocol-v2 QA

Independent read-only QA parsed 60 unique rows with 15 rows in each active arm
and reproduced matrix SHA-256
`f2a9019f093072e44e68b4f6dd8bab9abfe1655dd4b6ed94719ae54246786cf7`.
It confirmed exact seed/compute/pairing/provenance validation, fail-closed GRU and
H-04 exclusion, and preservation of historical GRU/HARTH evidence. Four focused
and all 28 Stage 09 tests passed; governance, notebook and diff checks passed.
The verdict is `PASS` for proposal consistency only. No data admission, training,
final access or numerical-rule freeze occurred.

## Statistical readiness audit

DEC-053 rehashed and parsed the existing Stage 08 Bike evidence. It contains one
Fly-like training seed, one Bike record, eight permutations and 0/10/30/50%
dropout rows, but no temporal-only comparator. Bike has four channels against
seen counts 11/26, so the evaluator emitted no channel-count rows and cannot
empirically calibrate registered views 18/370. Eight H-03 known-effect/failure
fixtures pass, but their rule values are not thresholds. M1 is `HOLD` pending a
PI choice of calibration budget and count-view basis; see `M1_CALIBRATION_AUDIT.md`.

DEC-054/055 then completed all six approved development runs. Each has 400 steps,
3,200 exposures and 68,760 parameters; locked report replay passes at SHA-256
`1bb8c7f9…e5b520`. Descriptive H-02 contrasts change sign across seeds and one
Bike record cannot justify the intended interval. The report also omits the
cross-arm clean reconstruction harm summary even though paired raw baselines are
preserved. See `M1_CALIBRATION_RESULT.md`; this triggered the final DEC-056 cycle.

DEC-056 v2 preserves the original report and recomputes the clean contrast, but
DEC-057 independent QA reports `FAIL` because replay depends on a live evaluation
config and exact run-directory validation accepts a numeric seed alias. Under the
final-cycle stop rule no further remediation is proposed; Stage 09 closure at
`HOLD` was accepted by the PI under DEC-058. A Draft PR is authorized for the
preserved package; no later research gate is opened.

- Stage 03's numerical values and 95% percentile intervals are candidates, not
  frozen rules. Its QA `PASS` applies to the evaluator and candidate report.
- Several Stage 03 interpolation views contain only one eligible domain and one
  source record. Those units cannot justify cross-domain uncertainty.
- H-03 requires a new paired hierarchical procedure with graph seed as the outer
  cluster and training seed as the inner unit, followed by a conjunctive IUT.
- H-04 probe tooling remains historical/synthetic coverage only and is excluded
  from protocol-v2 inference.
- Undefined norms/denominators, broken pairing, absent class coverage, inadequate
  independent units or failure to justify an exact value produce `HOLD` rather
  than an implementer-selected threshold.

## Required PI numerical packet

The later M2 gate must show, without final performance:

1. denominator and representation-norm floors;
2. H-01 view-specific permutation/count limits and uncertainty rules;
3. H-02 three dropout-rate effect limits and the 0% harm guard;
4. H-03 practical/adverse limits, interval construction and IUT decision rule;
5. interval level, resamples, independent units and undefined-result behavior.

No item in this list is frozen by this record.
