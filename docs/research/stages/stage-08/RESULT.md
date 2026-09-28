# Stage 08 Result — FlyTS-Mini Operational Pilot

Status: **closed — independent QA PASS; PI result GO**

Date: 2026-09-27

Draft PR: [#14](https://github.com/yhlee52/FlyTS_lab/pull/14) — open and unmerged

The DEC-032 fixed-order pilot completed once without a stop condition. The four
core arms each completed `200 + resume + 200` optimizer steps and 3,200 sample
exposures. The dense-leaky diagnostic completed `10 + resume + 10` steps and 160
sample exposures. Every run used CPU float32 with four threads, preserved and
hashed its resume-input checkpoint, selected the earliest minimum pretrain-domain
`L_select` checkpoint, and evaluated that checkpoint on Bike development data.

| Arm | Role | Parameters | Steps | Selected epoch | `L_select` |
|---|---|---:|---:|---:|---:|
| fly_like | core | 68,760 | 400 | 2 | 0.9713624630958333 |
| degree_preserving_rewired | core | 68,760 | 400 | 2 | 0.9710226302229774 |
| random_sparse | core | 68,760 | 400 | 2 | 0.9705458964618656 |
| gru | core | 68,853 | 400 | 2 | 0.9601946795740053 |
| dense_leaky | diagnostic | 68,530 | 20 | 2 | 0.9850482916142669 |

These are individual descriptive values from one seed, not a winner, mean,
significance result, acceptance threshold or Stage 09 budget decision. Bike results
did not select checkpoints or settings. Frozen-probe eligibility was audited only;
no frozen probe was run.

Strict schema-v2 report generation and byte-stable `--check` passed. The tracked
reports rehash the runner, reporter, package sources, pilot configs, manifest,
domain registry, evaluation fixtures and records, resource facts and all relevant
checkpoints. The canonical ignored run directory is
`outputs/stage08-pilot/pilot-20260927-v1/`; raw arrays, checkpoints and logs remain
outside Git.

The single-run CPU measurements show that degree-preserving rewiring setup dominates
its observed runtime: its two training-process setup phases total about 917 seconds,
compared with about 3–4 seconds for the other core arms. The report keeps setup,
training, validation, checkpoint and evaluation costs separate and gives linear
400/2,000/50,000-step five-seed scenarios. These scenarios retain measured fixed
costs per seed, scale only steady training-step time and are not performance or
budget guarantees.

The complete local test suite, Python compilation, report replay, notebook and
governance validators, `git diff --check`, and ignored-artifact checks pass. The
three CUDA tests are skipped because the environment is PyTorch 2.14.0+cpu.

Independent post-pilot QA returned `PASS` with no blockers. QA independently
matched all 15 best/last/snapshot hashes, fixed steps/exposure/parameters, finite
histories, earliest-minimum selection, Bike-only scope, common fixture, report byte
replay, tests, compilation, validators and artifact hygiene. QA did not rerun the
pilot or access Electricity arrays. Record-level target sums are not separately
persisted, so their aggregation was verified through implementation/tests and the
saved domain histories.

The PI issued result `GO` on 2026-09-28 and accepted this bounded operational
evidence package. Stage 08 is closed without expanding its claim scope.
Topology/backbone
superiority, robustness pass/fail, foundation quality, CUDA support, transfer and
semiconductor applicability remain `미검증`. Stage 09, final-held-out access and
merge remain unauthorized.

Under DEC-036, the reviewed Stage 08 changes were committed and Draft PR #14 was
opened on 2026-09-28. Both GitHub `pytest` checks on head `c09c0b5` passed in
2m13s and 3m40s. Merge remains a separate PI gate.
