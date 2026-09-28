# FlyTS-Mini v0.1 Research Preview — Known Limitations

## Release boundary

- This is an engineering/research preview with no pretrained checkpoint.
- Package `flyts 0.2.0` and research artifact `v0.1` are separate version axes.
- The release does not establish foundation-model quality or production readiness.
- Stage 09 remains `HOLD` and its final independent QA remains `FAIL`.

## Evidence limitations

- H-01–H-03 were not formally tested; their numerical rules were never frozen.
- H-04 is `not tested` because HARTH was not admitted.
- The Stage 08 pilot used one seed and 400 steps per core arm. Its loss values are
  descriptive operational evidence, not a ranking or model-selection result.
- The protocol-v2 60-run matrix is an unfrozen proposal and was never executed.
- Electricity final-held-out model evidence remains unopened.
- One Bike record and synthetic count fixtures cannot justify cross-domain or
  independent-unit uncertainty claims.

## Model limitations

- The current graph is fly-inspired and synthetic, not a measured connectome.
- The encoder has no explicit channel identity, unit or semantic metadata.
- Fully hidden semantically distinct channels may be ambiguous.
- Whole-window visible statistics make the encoder non-causal; streaming and
  online forecasting require a separate normalizer and stateful API.
- Patching can discard fine-grained information and has not been formally ablated.
- Full-window BPTT is used; AMP, multi-GPU and TBPTT are not implemented.
- Sparse topology is not guaranteed to be faster than dense execution.

## Data and task limitations

- The public corpus is small and domain coverage is limited.
- Entity transfer is not established where the same entity appears in chronological
  train/validation/test partitions.
- HAR is excluded by conflicting rights statements. HARTH is unadmitted because
  its registered test split lacks one class, cadence semantics conflict and its
  archive has no bundled notice.
- Checksums bind observed bytes but do not prove publisher authenticity, correct
  semantics or permission for every use.
- No public result demonstrates semiconductor or other company-domain transfer.

## Runtime and packaging limitations

- Recorded execution evidence is CPU float32. CUDA validation is not complete.
- Bitwise equality across operating systems, devices or PyTorch versions is not
  guaranteed.
- The offline bundle intentionally excludes a dependency wheelhouse and requires
  separately approved compatible NumPy/PyTorch dependencies.
- The same `flyts 0.2.0` package filename can represent different source builds;
  use the release manifest's commit/tree and SHA-256, not the filename alone.
- Bundle checksums provide integrity, not authentication. Preserve the manifest
  digest through a separate approved channel.

## Historical reporter limitation

Stage 09 `REPORT-v2` is not self-contained because it reads a live evaluation
config, and it does not reject a numeric run-directory alias such as `runs/07`.
Its QA verdict is `FAIL`. Prospective Stage 10 hardening applies only to future
declared-input replay and must not be described as repairing or passing Stage 09.

## Prohibited interpretations

Do not claim that Fly topology is superior, masking improves robustness, FlyTS is
a validated foundation model, public transfer is proven, Electricity performance
is known, CUDA is supported/validated, semiconductor data is supported, Stage 09
succeeded, or a pilot checkpoint is selected or optimal.
