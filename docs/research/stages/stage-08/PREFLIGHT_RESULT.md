# Stage 08 Schema-v2 Preflight Result

Status: **PASS — PI pilot-run gate pending**

Date: 2026-09-27

## Scope

DEC-031 authorized one common schema-v2 `1 + resume + 1` preflight for the four
core arms only. Dense, the 400-step pilot and final-held-out access were excluded.
Raw outputs are ignored under
`outputs/stage08-pilot/preflight-schema-v2-20260927/`.

## Operational evidence

| Arm | Steps | Samples | Parameters | Best epoch | Segment wall seconds |
|---|---:|---:|---:|---:|---|
| `fly_like` | 2 | 16 | 68,760 | 2 | 2.511 / 1.967 |
| `degree_preserving_rewired` | 2 | 16 | 68,760 | 2 | 259.328 / 532.540 |
| `random_sparse` | 2 | 16 | 68,760 | 2 | 2.005 / 2.151 |
| `gru` | 2 | 16 | 68,853 | 2 | 2.197 / 2.020 |

All histories were finite. Every arm preserved and hashed its epoch-1 resume
input, resumed in a separate process to epoch 2, used the approved manifest,
registry, config, seeds and parameter guard, and produced the same Bike-only
fixture `3370e2f3b6c6a8695024100cef607db5d582e059e5f271cffd59e666e6539bfa`.

The strict schema-v2 reporter independently rechecked package/tool/config/source,
input, checkpoint, resource, evaluator-record and fixture bindings plus execution
facts and earliest-best selection. Generation and `--check` matched exactly:

- `PREFLIGHT_RESULTS.json`:
  `e42a0df212c486e2c5a7564092fb1add243c71e57c9051d4e6d2bbab98fd590a`
- `PREFLIGHT_RESULTS.md`:
  `3017b584b7ab1c758664ffb2abb6b9633416aa84a101465e9cdcbbead53bba77`

The reporter must receive the resolved absolute `--runs` path because run facts
bind absolute execution paths. A relative invocation was rejected before report
creation; no training rerun or artifact mutation was needed.

## Interpretation

This is operational/descriptive evidence only. It does not establish a winner,
robustness pass/fail, topology/backbone superiority, foundation quality, CUDA,
transfer or semiconductor suitability. The degree-preserving process setup is
large; this preflight is not a Stage 09 cost estimate because one-step segments
do not provide a steady post-warmup step measurement.

## Gate

The common preflight gate is satisfied. The 400-step/20-step pilot remains
unauthorized pending a separate PI `GO`.
