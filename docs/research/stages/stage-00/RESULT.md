# Stage 00 Result — Baseline Reproduction

Status: review

Date: 2026-09-24
Baseline commit: `9a6f3d8d612f742815b1124f2a0c6ee1da544628`

## Conclusion

The merged foundation MVP baseline was reproduced on CPU without source, configuration, architecture, dataset, model-behavior, evaluation, scope, or acceptance changes. Installation, tests, synthetic smoke training, epoch-boundary resume, and embedding export completed. CUDA was measured as unavailable rather than inferred to work.

## Acceptance evidence

| Criterion | Result | Evidence |
|---|---|---|
| Reproducible installation | Pass | Project-local Python 3.12 environment and exact install commands in `docs/BASELINE_VALIDATION.md`. |
| Relevant tests | Pass | Governance validator passed; full pytest: 24 passed, 1 CUDA hardware skip. |
| CPU synthetic smoke | Pass | Two epochs, 17,936 parameters, finite train/validation losses. |
| Checkpoint resume | Pass | Epoch-boundary resume matched 29 model tensors bitwise and losses exactly. |
| Embedding export | Pass | Finite float32 embeddings `[9, 32]` reloaded without pickle. |
| CUDA status | Pass as unavailable | CPU-only PyTorch build, zero CUDA devices; no GPU claim. |
| Claims unchanged | Pass | Report explicitly limits results to synthetic CPU functionality. |
| Notebook validation | Pass | Governance validator and notebook validator pass after the Stage 00 refresh. |

## QA and limitations

Independent QA reproduced the core corpus, training, resume, export, test, and device evidence and issued `PASS` after independently revalidating the refreshed notebook. QA did not independently reinstall into a second environment or reproduce peak process memory. CUDA behavior, foundation-model quality, public-data performance, transfer, and topology benefit remain unverified.

## Artifacts

- Baseline report: `docs/BASELINE_VALIDATION.md`
- Independent QA: `docs/research/stages/stage-00/QA_REPORT.md`
- Ignored implementation artifacts: `outputs/phase0-baseline/`
- Ignored independent QA artifacts: `outputs/phase0-baseline/qa/`

No PR is merged and Stage 01 has not begun.
