# Stage 05 Result — Topology Controls

Status: review

Date: 2026-09-26

## Question and conclusion

The three registered topology arms can be deterministically generated, validated,
restored, and exercised through the same schema-v1 artifact and Foundation path
under the approved structural, seed, and provenance contract. Independent QA reports
`PASS`. This is engineering and structural evidence only; it does not test H-03 or
support a topology-performance claim.

## Work completed

- Added uniform directed degree-preserving rewiring and fixed-edge random sparse
  controls with bounded deterministic failure and no seed/candidate selection.
- Preserved common N/E, annotations, model path, parameter count/order and paired
  initialization; overlap and Jaccard remain descriptive under DEC-019.
- Added the minimal control-seed config, format-v1 graph/run/checkpoint provenance,
  exact regenerated-buffer validation, legacy loading and cross-topology rejection.
- Added fixed structural fixtures, CPU dense/scatter one-step tests, source-hashed
  JSON/Markdown reports and the public control contract.

## Evidence

| Evidence | Result | Artifact |
|---|---|---|
| Fixed graphs | 613 edges per arm; stable hashes | `reports/topology/stage05-controls.json` |
| Rewired contract | 6,130 accepted / 11,235 proposals; exact in/out degrees | report and focused tests |
| Random contract | candidate 1; exact N/E, incoming/component guards | report and focused tests |
| Model/checkpoint | paired parameters; finite dense/scatter step; strict v1 and buffer guards | `tests/test_topology_controls.py` |
| Regression suite | focused 60 passed/2 skipped; full 76 passed/3 skipped | `QA_REPORT.md` |
| Reproducibility | source commit/path hashes, report `--check`, validators and clean diff/status | tracked report and QA |
| Delivery CI | two GitHub `pytest` checks passed on Draft PR #11 head `433f9b2` | Draft PR #11 |

## Acceptance criteria

- [x] Stage 04 fly-like graph/state/parameter/checkpoint contracts remain unchanged.
- [x] All arms match N/E, annotations, trainable parameter contract and deterministic hashes.
- [x] Rewired satisfies exact degrees/components and `10E/200E`; overlap is descriptive.
- [x] Random satisfies fixed-edge, incoming/component and role-distinction guards.
- [x] Global RNG isolation and paired trainable initialization are verified.
- [x] Dense/scatter finite CPU forward/backward/optimizer-step checks pass.
- [x] Legacy/new format-v1 provenance, buffer mismatch and resume guards pass.
- [x] Tracked reports, focused/full tests, validators and independent QA `PASS`.

## QA verdict

Independent final QA issued `PASS` after two provenance defects were corrected and
the user approved one extra bounded QA follow-up in DEC-020.

## Unverified claims and risks

- H-03, topology superiority, robustness, transfer, foundation quality, CUDA,
  biological mechanism and semiconductor suitability remain `미검증`.
- Exact replay of an in-place resume requires retaining the pre-resume checkpoint;
  the current provenance records the exact invocation but does not archive that input.
- The structural fixture is one fixed graph configuration, not evidence over graph
  sizes, datasets, training budgets, or performance seeds.

## Decisions recorded

- DEC-018 approved the Stage 05 scope and fixed generator/provenance contract.
- DEC-019 retained uniform rewiring while making overlap/Jaccard descriptive.
- DEC-020 approved one extra bounded independent QA follow-up.

## Pull request

- Draft PR: #11 (`codex/stage-05-topology-controls` -> `main`).
- Merge and Stage 06 remain separately gated.

## User stage gate

- Requested: `GO`, `REVISE`, `HOLD`, or `STOP`.
- Decision: pending.
