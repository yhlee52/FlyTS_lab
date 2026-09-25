# Stage 03 Result — Foundation Robustness Evaluator

Status: closed

Date: 2026-09-25
Stage gate: user-approved closure without numerical freeze; independent final QA `PASS`.

## Conclusion

The offline evaluator and exact-hash public development calibration candidate satisfy the eight Charter acceptance criteria within the user-approved no-frozen-threshold scope. Independent final QA reported `PASS — approved evaluator and candidate deliverables under no-frozen-threshold closure`; Stage 03 is closed (DEC-014–015). Thresholds, numerical guards and uncertainty configuration remain `candidate` and unfrozen. Robustness values are descriptive; no pass/fail, foundation-quality, transfer, topology or CUDA claim follows from them.

## Charter acceptance evidence

| Criterion | Final assessment | Evidence |
|---|---|---|
| Deterministic stable results and ordering | Met | `tests/test_evaluation.py`; ignored `outputs/stage03/eval-seed*/summary.json` and `records.jsonl` |
| Smooth L1 `beta=1.0`, valid targets, position→record→domain macro | Met | `src/flyts/evaluation.py`, `docs/EVALUATION.md`, weighted-record regression tests |
| Paired shared target and sealed test/final-held-out | Met | Paired fixture tests; explicit role/split errors and test-array-not-open regression |
| Identity, permutation, dropout, count, padding, missing and guards | Met for evaluator controls | Focused CPU tests; algebraic sensitivity references in candidate report are not executed empirical fixtures |
| Versioned schema, provenance and numeric report consistency | Met | `schemas/robustness-result-v1.schema.json`, candidate JSON/CSV/Markdown and source/fixture hashes |
| Focused/full suite and governance validation | Met; final QA `PASS` | Focused 19 passed/one CUDA skip; full 55 passed/three CUDA skips; notebook/governance validators and `git diff --check` passed; `QA_REPORT.md` |
| Three-seed bounded public calibration candidate | Met | Exact manifest, seeds `7/17/29`, 400 steps each with uniform `last.pt`, 522 val windows/seed, 38,634 raw rows/seed, 31 metric arms, 10,000 paired hierarchical bootstrap resamples |
| Independent candidate QA | Met within no-freeze closure scope | Pre-remediation `CONDITIONAL PASS`, remediation `PASS`, and final independent QA `PASS`; `QA_REPORT.md` |

## Provenance

| Item | SHA-256 or identity |
|---|---|
| Base `main` commit | `461f1fc1dc1c809a9486dc36a70e3f942e5d309c` |
| Public starter manifest | `e538e9cbf761577740f43f6930ac4653834fdc00f9d0ee567b02b52e2d0d14eb` |
| Evaluator config | `8495082014eb539e64c7671cc9227509b3769c4709a954f5dade71ced09e1211` |
| Evaluator source at calibration | `e8417668ddb02f8ecf900df40a202e9427ba46f80ddbcf0fb46314f2577574f1` |
| Paired fixture | `d48087dac8456d191a277c6e59421798a679e4079ca2e859faa398bde6324f0f` |
| Seed 7 `last.pt` | `4a281462a7117f4fec33a844b8faa7e1046227c108c4da513d01da147205897e` |
| Seed 17 `last.pt` | `16190ea89458742410682319448bce2491f0993e560ada828fda03b0f4ec1224` |
| Seed 29 `last.pt` | `cce6cb1e0ab940fde7168c132b3735472ab75486dc296825f3af6a9e9c55947a` |

Full seed-specific training config and raw-result hashes are in `reports/robustness/calibration-candidate-v1.json`. Training and evaluation read train/val only; `test` and final-held-out were excluded. `best.pt` is not used as a Stage 01 primary-selection claim.

## Candidate interpretation and limits

The evaluator produced finite descriptive values, but the development evidence does not justify a numerical effect-threshold freeze. Three interpolation count arms have one eligible domain and one source record; an algebraic order-sensitive formula reference is not an executed sensitivity fixture. This is an interpretable insufficient-calibration outcome, not evidence that the encoder succeeds or fails robustness. The three-domain/three-seed intervals are candidate uncertainty descriptions and do not establish generalization to final-held-out domains.

CUDA execution, formal pass/fail thresholds, frozen probes, transfer, topology effects, final-test behavior and foundation-model quality remain `미검증`.

## Artifacts and next gate

- Evaluator contract: `docs/EVALUATION.md`; CLI/core: `src/flyts/__main__.py`, `src/flyts/evaluation.py`.
- Candidate summary: `reports/robustness/calibration-candidate-v1.{json,csv,md}`.
- Raw rows, checkpoints and run logs: ignored `outputs/stage03/`.
- Charter and decision: `docs/research/stages/stage-03/CHARTER.md`, DEC-011–014.
- Independent final QA: `docs/research/stages/stage-03/QA_REPORT.md` (`PASS` within the no-freeze scope).

The Research Director may prepare the user-authorized Draft PR. Merge and Stage 04 require separate user approval. Formal robustness pass/fail requires a separately approved reopening and numerical freeze.
