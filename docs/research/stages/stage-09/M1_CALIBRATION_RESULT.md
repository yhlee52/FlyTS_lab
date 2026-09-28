# Stage 09A M1 Calibration Result

Status: **HOLD — DEC-057 final reporter QA FAIL**

Date: 2026-09-28

## Execution

DEC-054 completed exactly six development runs: seeds `7/17/29` crossed with
`fly_like` and `temporal_only`. Every run used CPU float32/four threads, batch 8,
400 optimizer steps, 3,200 exposures and 68,760 parameters. Each run preserved a
process-boundary checkpoint after 200 steps and selected epoch 2 as its earliest
minimum. Training used only Appliances/Beijing; evaluation used one Bike
validation record. No Electricity, HARTH, H-04, GRU or final/test asset was used.

Ignored evidence root: `outputs/stage09/dec054-calibration-v1/`.

| Artifact | SHA-256 |
|---|---|
| `plan.json` | `d428b60cf4bca0f688b0cfe47a5d79e60df79caa49505d29f058f70466d360ca` |
| `synthetic_h01.json` | `4c4a0e4e26d641cc90149924a7affbc1178dabda63d915b490c97657bd93f0b8` |
| `REPORT.json` | `1bb8c7f9d1811ee0caceaaabbb65f146ee892e2f0e84bb88433fb5b844e5b520` |

Read-only `--check` reproduced the locked report byte-for-byte. The focused
calibration plus Stage 09 readiness suite reports 33 passed.

## Descriptive evidence

All eight Bike permutation views are finite. Their per-run domain-macro values
range from `5.1660e-09` to `5.3013e-08`. These values are descriptive numerical
behavior from one Bike record and do not select an invariance threshold.

For H-02, the descriptive paired contrast below is temporal-only degradation
minus masked Fly-like degradation. Positive values favor the masked arm; no
effect or uncertainty rule is applied.

| Seed | 10% | 30% | 50% |
|---:|---:|---:|---:|
| 7 | `0.00024255` | `-0.00082150` | `0.00026705` |
| 17 | `0.00107816` | `0.00246833` | `0.00526125` |
| 29 | `0.00017277` | `-0.00169602` | `-0.00370229` |

Signs disagree across seeds at 30% and 50%. With one Bike record, these results
do not justify an independent-unit interval or practical-effect threshold.

The synthetic H-01 count fixtures cover `4/18/370`, nearest seen counts `11/26`,
null, sensitivity, undefined denominator and all-view conjunction behavior. They
are explicitly non-empirical and cannot establish final count-view performance.

## Reporter defect and gate

The locked report records dropout 0% relative degradation as zero, which is true
by construction, but does not summarize the registered cross-arm clean
reconstruction harm guard. The preserved paired raw rows contain finite absolute
baselines with identical fixture IDs and target counts. A read-only diagnostic
found temporal-only minus masked relative clean changes of `-0.00175771`,
`0.00164310` and `0.00013200` for seeds `7/17/29`.

This is a reporter omission discovered after execution. It does not create false
support because `REPORT.json` remains `HOLD` with `exact_rules=null`, but the
package cannot become an M2 packet until an authorized remediation adds the
prespecified clean-harm summary from existing rows and independent QA validates
the complete evidence. No rerun or threshold selection is authorized here.

DEC-056 created a versioned `REPORT-v2.json` without changing the original. Its
SHA-256 is `8ab632b54e36c22ee7bc89212e53904092dba3cfa6e8fc0bc29a7285b4760db3`,
and its clean-loss arithmetic matches independent recomputation. DEC-057 QA still
reports `FAIL`: v2 reads a live evaluation config outside the approved preserved
input set and does not reject a numeric seed-directory alias such as `07`.

## Conclusion

M1 and Stage 09 remain `HOLD`. H-01/H-02 values are descriptive; H-03 fixtures
validate implementation only. Under the final-cycle stop rule no further repair
is proposed. Under DEC-058 the PI accepted Stage 09 `HOLD` closure and authorized
a Draft PR of the preserved package. M2, M5/M6, final opening, claims, merge and
Stage 10 remain closed.
