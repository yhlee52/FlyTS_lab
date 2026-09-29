# FlyTS-Mini v0.1 Research Preview — Model Card

## Release status

This is an engineering/research preview, not a validated foundation model or a
production model. It publishes source, configs and reproducibility tooling but no
pretrained checkpoint. Formal training, formal comparison, final-held-out
evaluation and transfer validation are incomplete.

| Identity | Value |
|---|---|
| Research artifact | `FlyTS-Mini v0.1 Research Preview` |
| Python package | `flyts 0.2.0` |
| Candidate tag | `flyts-mini-v0.1-preview.1` |
| Checkpoint | none published |
| Stage 09 | closed `HOLD`; final independent QA `FAIL` |
| Hardware evidence | CPU float32; CUDA not tested |

The package and research artifact use separate version axes. A package filename
alone is insufficient provenance; use the release manifest's source tree and
artifact SHA-256.

## Intended use

- Research and engineering inspection of a variable-channel multivariate
  time-series encoder.
- Reproduction of the documented synthetic CPU smoke, save/load/resume, embedding
  and public-data preparation paths.
- Development of leakage-safe channel masking, replaceable topology controls and
  offline-first workflows.
- A starting point for a separately preregistered formal study.

## Non-intended use

- Production, safety-critical, clinical, financial or automated operational use.
- Treating the package as a pretrained or generally capable time-series foundation
  model; no pretrained checkpoint is distributed.
- Selecting FlyTS over GRU, rewired, random or other backbones based on performance.
- Claiming robustness to physical sensor failures, zero-shot/domain transfer,
  Electricity performance, CUDA readiness or semiconductor suitability.
- Online/causal forecasting: the current encoder uses whole-window visible context
  and is non-causal.
- Using a Stage 08 pilot checkpoint as an optimal, selected or validated model.

## Architecture

FlyTS accepts `[batch, time, channel]` inputs and uses a shared patch tokenizer,
learned slot-based channel mixer/router, a recurrent backbone and contextual
reconstruction head. The current Fly path uses a fly-inspired synthetic population
graph, not a measured FlyWire connectome. Alternative rewired, random sparse,
dense-leaky and GRU engineering paths exist for controlled research.

The design separates original missingness, padding and artificial masking. Fitted
normalization uses training-visible observations; reconstruction loss applies only
to valid, originally observed hidden targets. Sensor identity, unit and semantic
metadata are not modeled explicitly, so waveform-equivalent channels with different
physical meaning may be indistinguishable.

## Data and roles

The admitted Stage 06 corpus roles are fixed:

| Domain | Role | Preview use |
|---|---|---|
| Appliances | pretrain | public preparation/training path |
| Beijing Multi-Site | pretrain | public preparation/training path |
| Bike Sharing | development-held-out | development/evaluator evidence only |
| ElectricityLoadDiagrams20112014 | final-held-out | sealed; no model result opened |

Raw public datasets are not distributed in the preview. The repository provides
official-source references, recorded rights statements, checksums where approved,
attribution and download/prepare procedures. Rights statements are not legal
advice; review source archives and notices for the intended use.

HAR is excluded from the default corpus because its bundled use restriction and
current landing-page license statement conflict. HARTH is unadmitted: its only
registered split lacks one official test class, one subject has conflicting cadence
semantics and the official archive lacks a bundled notice. No HARTH arrays, windows
or probes are part of this preview.

Company and semiconductor data, paths, metadata, checkpoints and embeddings are
not public artifacts and must not be uploaded.

## Training and evaluation status

- Stages 0–7 established bounded engineering paths with stage-specific QA.
- Stage 08 completed a one-seed, 400-step-per-core-arm CPU operational pilot with
  independent QA `PASS`. It is descriptive pipeline evidence, not performance or
  model-selection evidence.
- Stage 09 ended at `HOLD`. Its 60-run protocol-v2 matrix remains an unfrozen
  proposal. Numerical rules, formal training, final opening and formal analysis
  did not occur.
- H-01, H-02 and H-03 have no formal result. H-04 was not tested because HARTH was
  not admitted.
- The final Stage 09 reporter QA is `FAIL`: historical `REPORT-v2` depends on a
  live evaluation config and accepts a numeric seed-directory alias. Stage 10 may
  harden future tooling but does not revise this historical verdict.

## Checkpoint availability

No pretrained checkpoint is published. Checkpoints created during documented CPU
smoke or user-run training are local outputs and are excluded from release assets.
Unknown or untrusted checkpoints must not be loaded or transferred as if approved.

## Hardware and reproducibility

Recorded operational evidence used CPU float32. The code accepts a CUDA device and
contains CUDA tests, but the current environment lacks CUDA hardware and those
tests are skipped. This preview therefore makes no CUDA validation, performance,
memory or compatibility claim.

The offline bundle contains project source/package artifacts, exact supported
configs, documentation, a synthetic fixture and integrity metadata. It is not a
dependency wheelhouse. Compatible NumPy/PyTorch dependencies and the target
OS/Python/device contract must be supplied and approved separately.

## Evidence tiers

- **Verified engineering:** independently tested code and execution paths within
  their recorded environment and scope.
- **Operational pilot:** Stage 08 single-seed descriptive evidence.
- **Development-only:** Stage 03/09 calibration and candidate evidence.
- **HOLD/failed QA:** unresolved Stage 09 evidence and reporter defects.
- **Not tested:** formal/final inference, transfer, CUDA and semiconductor use.

See `reports/EVIDENCE_MATRIX.md` for path-level classification. A tooling `PASS`
does not convert a scientific `HOLD`, `FAIL` or `not tested` status into support.

## Known limitations and risks

- No formal evidence establishes channel-count generalization, channel-order
  invariance, masking benefit, topology benefit or reusable representations.
- Public data covers few domains and independent units; it is not web-scale or
  representative of industrial time series.
- The encoder is non-causal and does not provide streaming state or forecasting.
- Sampling semantics, sensor meaning and units require dataset-specific review.
- Sparse/recurrent efficiency and CUDA behavior are not established.
- Checksums demonstrate integrity, not publisher authenticity or legal permission.

Additional details are in `docs/KNOWN_LIMITATIONS.md`.

## Ethical, security and rights considerations

- Do not include private/company paths, raw data, checkpoints, embeddings, IDs or
  sensitive metadata in public archives.
- Preserve dataset attribution, bundled notices, official-source URLs and observed
  hashes. Exclude material when rights or schema are ambiguous.
- Avoid claims that could encourage unvalidated deployment or semiconductor use.
- Verify archives against the release manifest and obtain their digest through an
  approved channel; a modified manifest plus modified files defeats checksum-only
  authentication.

## Semiconductor boundary

This preview provides no evidence that FlyTS is suitable for semiconductor
equipment data. Semiconductor adaptation is deferred until a later, separately
approved cycle after adequate public-data validation. Public engineering success
must not be interpreted as company-data compatibility, safety or transfer.
