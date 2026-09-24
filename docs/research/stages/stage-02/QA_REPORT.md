# Stage 02 Independent QA Report

Date: 2026-09-25
Final verdict: `PASS`

## Initial review and remediation

Initial QA issued `FAIL` for forced minimum-one channel targets, unclear target-free single-channel handling, incomplete manual-plan validation, missing/padding conflation, an abbreviated charter, incomplete stage records, and missing focused reproductions. The one approved implementation follow-up corrected these bounded defects without changing the masking contract. The initial verdict is retained here rather than overwritten.

## Independent follow-up evidence

- Low-ratio `C=2` sampling produced 97 zero-channel and three one-channel selections across 100 seeded records; it no longer forces masking.
- All-hidden, partial-channel, partial-dropout, and channel/dropout-overlap manual plans raise clear errors.
- Real missingness, time padding, and batch channel padding are distinct through `channel_counts`; partial patches exclude padding.
- `C=1` model forward remains valid, while target-free channel-only training raises the documented incompatibility error.
- Focused masking/foundation/pipeline tests and the full suite pass: 36 passed, two CUDA hardware skips.
- An independent two-epoch synthetic CPU smoke produced finite losses with 17,936 parameters.
- Epoch-boundary resume reproduced all 29 model-state tensors bitwise and retained checkpoint format version 1.
- Notebook and governance validators and `git diff --check` pass.

## Limitations

CUDA remains unverified. Stage 03 dropout degradation, evaluator thresholds and uncertainty, representation quality, topology benefit, and final-test performance remain unverified. Fully hidden channels remain indistinguishable without metadata. Channel-only masking can legitimately produce a target-free batch at low ratios or `C=1`; training fails explicitly and recommends positive temporal masking.
