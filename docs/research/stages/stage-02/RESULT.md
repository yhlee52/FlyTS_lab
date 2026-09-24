# Stage 02 Result — Channel Masking and Channel Dropout

Status: review

Date: 2026-09-25
Base commit: `8addce5f24785cf4438c4f9136046637e2ba2563`

## Conclusion

Stage 02 implements the approved masking mechanics, leakage guards, compatibility path, and CPU reproducibility evidence. Initial independent QA `FAIL` findings were corrected through the single bounded follow-up, and final independent QA is `PASS`. This functional result is not evidence of performance improvement or foundation-model quality.

## Acceptance evidence

| Criterion | Result | Evidence |
|---|---|---|
| Seeded masking and low-ratio rounding | Pass | Deterministic cause masks; different seeds can differ; low ratios may round to zero. |
| Legacy and checkpoint compatibility | Pass | Exact temporal sampler preserved; legacy/nested equivalent resume; checkpoint format v1. |
| Config validation | Pass | Exclusive legacy/nested forms, ratio guards, and incompatible resume errors. |
| Edge conditions | Pass | `C=1` no-op, precise target-free error, 50% dropout forward, partial/all-missing handling. |
| Mask algebra and padding | Pass | Full-channel causes, union target, overlap ownership, visible guard, separate missing/time/channel padding. |
| Leakage prevention | Pass | Hidden/dropped perturbations do not affect visible context; pooled record-visible fallback is target-independent. |
| Equivariance and CPU execution | Pass | Paired channel permutation, finite forward/backward, two-epoch CPU smoke. |
| Reproducibility | Pass | Uninterrupted and epoch-resumed training match all 29 model tensors bitwise. |
| QA and governance | Pass | Final independent QA `PASS`; 36 tests pass, two CUDA skips; validators, diff check, and Draft PR #8 Actions `tests` run #40 pass. |

## Artifacts and limitations

- Contract: `docs/MASKING.md`
- Configuration: `configs/stage02_smoke.json`
- Independent QA: `docs/research/stages/stage-02/QA_REPORT.md`
- Draft PR: `https://github.com/yhlee52/FlyTS_lab/pull/8`

CUDA, numerical robustness thresholds, Stage 03 evaluator behavior, representation quality, topology benefit, and final-test performance remain `미검증`. Fully hidden channels cannot be distinguished without metadata. Stage 03 has not begun, and the Stage 02 result gate remains pending.
