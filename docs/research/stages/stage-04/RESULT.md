# Stage 04 Result — Topology Modularization

Status: closed

Date: 2026-09-25

## Question and conclusion

The existing synthetic fly-like graph can be extracted behind a reusable topology artifact and builder without changing the registered graph, Foundation state contract, same-backend CPU numerical behavior, format-v1 checkpoint path, training resume or evaluator rows. Independent QA reports `PASS`. This is compatibility evidence only; it does not support a topology-performance claim.

## Work completed

- Added a validated, immutable CPU `GraphArtifact`, exact `fly_like` builder, canonical content hash and descriptive graph statistics under `src/flyts/topology/`.
- Routed Foundation graph construction through the topology package while retaining `_make_fly_mask` as the legacy wrapper.
- Added the `EncoderConfig.topology="fly_like"` default and canonicalized missing topology fields during format-v1 resume comparison without changing the checkpoint version.
- Added portable graph/state/parameter fixtures and focused load, resume and evaluator compatibility tests.
- Documented the interface, direction convention, persisted-state boundary and limitations in `docs/TOPOLOGY.md`.

## Evidence

| Evidence | Artifact | Interpretation |
|---|---|---|
| Five legacy seeded graphs | `tests/fixtures/stage04_fly_like_golden.json` | Edge count and ordered edge hash match the pre-refactor implementation. |
| State and parameter contract | `tests/test_topology.py` | Keys, shapes, dtypes, registration order and 936-parameter fixture remain fixed. |
| CPU numerical snapshot | ignored `outputs/stage04/{baseline.pt,compare.py}` | State/order/forward/loss/gradients are bitwise on the same CPU backend. |
| Checkpoint/training/evaluator compatibility | `tests/test_topology.py` | Strict format-v1 load, bitwise epoch resume and stable evaluator rows pass with a missing legacy topology field. |
| Regression suite | test and validator commands | 13 focused passed; full suite 68 passed/three CUDA skips; notebook, governance and diff checks pass. |

## Acceptance criteria

- [x] Exact legacy graph and validated artifact/statistics interface.
- [x] State, parameter and same-backend CPU numerical compatibility.
- [x] Strict format-v1 load and canonical legacy resume.
- [x] Dense/scatter, runtime checkpoint, training/resume and evaluator coverage.
- [x] Focused/full tests and validators with independent QA `PASS`.

## QA verdict

Independent QA issued final `PASS` after the shared notebook's stale test count was corrected. No graph, model, checkpoint, training, evaluator, leakage or scope regression was reproduced.

## Unverified claims and risks

- CUDA remains unverified on unavailable hardware.
- The full pre-refactor numerical snapshot is local ignored evidence; committed tests preserve its portable structural and behavioral contracts.
- Topology superiority, foundation-model quality, transfer and semiconductor suitability remain unverified.
- Rewired/random controls and topology comparisons belong to Stage 05 and are not implemented here.

## User decisions and delegated choices

- DEC-016: user `GO` approved the bounded Stage 04 extraction and exact compatibility contract on 2026-09-25.

## Decisions recorded

- Checkpoint format remains version 1; only `fly_like` is registered in Stage 04.
- No dataset, split, metric, numerical-threshold or scientific-claim change was made.

## Pull request and integration

- Draft PR #10: `https://github.com/yhlee52/FlyTS_lab/pull/10`
- Initial implementation and result commit: `c4fdc62`
- GitHub Actions `pytest` run `36106979369`: passed on record commit `8563df3` before this CI evidence note.
- PR #10 was subsequently merged into `main` at `944f8ed` on 2026-09-25. This integration fact does not retroactively alter the Stage 04 decision boundary; Stage 05 was separately approved in DEC-018.

## User stage gate

- Requested: `GO`, `REVISE`, `HOLD`, or `STOP`.
- Decision: `GO`, 2026-09-25.
- Conditions: Stage 04 result accepted and Draft PR requested. Merge and Stage 05 remain separately gated.
