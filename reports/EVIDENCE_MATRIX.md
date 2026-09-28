# FlyTS-Mini v0.1 Research Preview — Evidence Matrix

Status: Stage 10 release-candidate classification under DEC-060/061

This matrix separates release classification, evidence tier and QA/scientific
status. `PASS`, `HOLD`, `FAIL` and `not tested` are not interchangeable. Inclusion
in the source archive does not make an experimental or archived path
release-supported.

## Release inventory

| Path or artifact group | Release classification | Evidence tier | Recorded status | Preview treatment |
|---|---|---|---|---|
| Core package excluding formal-study interpretation (`src/flyts/` tokenizer, masking, topology, backbones, corpus, training, evaluation and CLI paths) | release-supported | Verified engineering | prior independent QA `PASS`; Stage 10 QA pending | include as source/package; support only documented engineering behavior |
| `configs/smoke.json`, `configs/cpu.json`, `configs/full_pretrain.json`, public source/hash and role configs | release-supported | Verified engineering | configuration/schema tests pass; no performance result | include exact bytes; label `full_pretrain` as a budget preset, not a validated model recipe |
| `tools/offline_bundle.py`, corpus pack/unpack/verify and offline documentation | release-supported | Verified engineering | MVP path recorded; Stage 10 clean-room QA pending | include and independently seal/verify |
| Synthetic fixtures and unit/integration tests | release-supported | Verified engineering | prior suites pass; Stage 10 rerun pending | include small fixtures and tests; synthetic results make no model-quality claim |
| Stage 00–07 reports, configs and QA records | archived evidence | Verified engineering | stage-specific `PASS`/PI decisions | retain in source archive; do not present as current performance evidence |
| Stage 08 configs, reports and local pilot description | archived evidence | Operational pilot | independent QA `PASS`; one seed only | retain tracked report/configs; exclude ignored runs/checkpoints; no winner or selection claim |
| Stage 03 and Stage 09 calibration configs/reports | archived evidence | Development-only | descriptive/candidate; rules unfrozen | retain for provenance; no threshold, robustness or formal claim |
| Stage 09 60-row matrix, cache/unseal and formal tooling | experimental | Development-only | proposal consistency QA `PASS`; never frozen or formally run | retain source with experimental label; exclude from release-supported workflow |
| Stage 09 `REPORT-v2` historical remediation | known-broken/unsupported | HOLD/failed QA | final independent QA `FAIL` | preserve original result/hashes; never claim replay support for the historical artifact |
| Prospective reporter after Stage 10 hardening | experimental until M9 | Verified engineering only after new QA | Stage 10 QA pending | support only future declared-input replay; it cannot repair Stage 09 retrospectively |
| Stage 08/09 ignored run directories, raw rows, resource logs and graphs | local-only | Operational/development evidence | not release-audited as public assets | exclude from every public candidate |
| Public dataset archives and prepared arrays | local-only | source/manifest provenance only | rights statements recorded per dataset | exclude bytes; include official source, attribution, checksum references and prepare instructions |
| HAR/HARTH data or derived arrays | excluded for rights/security | HOLD/failed QA | HAR rights conflict; HARTH unadmitted | exclude bytes and derived artifacts; retain limitations and historical metadata only |
| Electricity arrays and model outputs | excluded for protocol/security | Not tested | final-held-out unopened | exclude; no score, result or performance statement |
| Stage 08 pilot or any other checkpoint/embedding | local-only and excluded | Operational pilot at most | no selected/validated checkpoint | exclude; model card says no pretrained checkpoint is available |
| Company data, metadata, checkpoints or paths | excluded for rights/security | Not tested | outside public project evidence | prohibit from repository and archives |
| CUDA execution and device artifacts | unverified | Not tested | CUDA tests skipped in CPU environment | record skips; do not publish a CUDA support/validation claim |
| Dependency wheelhouse | unverified and excluded | Not tested | no target OS/Python/PyTorch/device contract | exclude; handle only in a later target-specific approval |
| Wheel/sdist, source archive, offline bundle and release manifest | release-supported after M8; M9 pending | Verified engineering | M8 `PASS`; Stage 10 QA pending | byte-stable ignored candidates are hash-bound; publish only after post-merge rebuild and M10B `GO` |

## Hypothesis and requirement evidence

| Item | Available evidence | Scientific status | Permitted statement |
|---|---|---|---|
| H-01 / R-01, R-02 | mechanics, evaluator tests and development-only descriptive values | `HOLD`; no formal/final inference | variable-channel and permutation evaluation paths are implemented; generalization/invariance support is unproven |
| H-02 / R-04 | masking/leakage tests and development-only paired calibration | `HOLD`; no formal/final inference | missing-channel training/evaluation mechanics exist; robustness improvement is unproven |
| H-03 / R-05 | topology controls, matching tools and unfrozen formal proposal | `HOLD`; no formal result | topology can be swapped and controlled structurally; topology benefit is unproven |
| H-04 | HARTH admission failure and no target test | `not tested` | no public-domain transfer or foundation-representation claim |
| R-06 | CPU runs and tests; CUDA skipped | CPU engineering evidence only; CUDA `not tested` | CPU path is exercised; CUDA validation is pending |
| R-07 | no-network design, corpus bundle and seal/verify tool | M8 engineering `PASS`; Stage 10 QA pending | offline workflow passed within the recorded dependency and bundle limits |
| R-08 | semiconductor work deliberately deferred | `not tested` | no semiconductor suitability or transfer statement |

## Claim boundary

The preview may state:

> FlyTS provides a reproducible engineering MVP and public-data operational
> pipeline for variable-channel time series. Formal comparison, final-held-out
> evaluation, transfer validation and pretrained checkpoint publication are not
> complete.

It must not state or imply that Fly topology or masking is superior, FlyTS is a
validated foundation/production model, public transfer is established,
Electricity performance is known, CUDA is validated, semiconductor data is
supported, Stage 09 succeeded, or a Stage 08 checkpoint is selected or optimal.
