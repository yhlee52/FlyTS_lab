# Stage 10 M8 Clean-room Reproducibility

Status: **PASS — pre-integration candidate; independent M9 QA pending**

Date: 2026-09-29

## Identity and environment

- Source commit: `14f95c9906bb771783686072d7cd0553094cc491`
- Source tree: `f2a50014f3d9870a9e88ed2554e1d8f40d84fd4c`
- Python: 3.12.14
- PyTorch: 2.14.0+cpu
- NumPy: 2.5.3
- Device: CPU float32; CUDA hardware unavailable and not tested
- Package/research versions: `flyts 0.2.0` / `FlyTS-Mini v0.1 Research Preview`

The build used two fresh extractions of `git archive` for the source commit with
`SOURCE_DATE_EPOCH=0`. The release builder reads source bytes from Git objects,
normalizes sdist tar/gzip metadata and rejects a dirty checkout.

## Candidate checksums

| Asset | SHA-256 |
|---|---|
| `flyts-0.2.0-py3-none-any.whl` | `34b5f677321a10a8721fc53faa53fbae7086c3ed8a789f1583f11fc64ffca7e1` |
| `flyts-0.2.0.tar.gz` | `11c392bf364f1982562d327971c57151a9a79004a7b4df1f924e914dd4effaf4` |
| `flyts-mini-v0.1-preview.1-manifest.json` | `bce6a87c56e992e6252769c901614e4223abd28680471dabcb68814361cc5ecf` |
| `flyts-mini-v0.1-preview.1-offline.zip` | `5fb6ba3fbaed5c0c2dc6836fce47143e367328fb53b1db2561b546258a2964a5` |
| `flyts-mini-v0.1-preview.1-source.tar.gz` | `4fa61176aec54c1dc51f2a72761ee51803f0058495cc76be986aaba1b6c7060c` |

`SHA256SUMS` also binds the manifest. Two independently built package inputs
produced byte-identical sealed source, wheel, normalized sdist, offline bundle,
manifest and checksum files. Both candidate directories passed the release
tool's seal/verify operation.

The tracked `reports/releases/flyts-mini-v0.1-preview.1/manifest.json` is this
pre-integration snapshot. Because a manifest cannot self-bind the commit that
adds itself and the later QA report, M10B must regenerate the external release
manifest and every asset from the user-merged `main` commit before tagging.

## Installation and CLI

- Wheel and sdist were installed separately into new virtual environments with
  `--no-index --no-deps`; sdist used `--no-build-isolation --no-cache-dir`.
- The environments were given only the already-approved compatible CPU
  NumPy/PyTorch dependency path. No dependency wheelhouse is claimed or bundled.
- `pip check` returned `No broken requirements found` in both environments.
- Both imports resolved to their new environment's installed `flyts` package,
  not the repository source, and both `python -m flyts --help` outputs matched
  the documented command set.

## CPU and offline paths

- Installed-wheel synthetic generation produced 24 records (16 train, four
  validation, four test) and corpus verification passed.
- A two-epoch CPU smoke pretrain completed with 17,936 parameters. A one-epoch
  checkpoint resumed to epoch two; its model tensors and history excluding the
  intentionally variable `seconds` field exactly matched the continuous run.
- Validation embedding export completed with four embeddings.
- Installed-sdist synthetic generation and corpus verification passed separately.
- The no-network pipeline test replaces socket connection with a hard failure and
  passed; candidate installation used `--no-index`. Only `flyts fetch` is an
  online command.
- Prospective reporter tests passed without a live evaluation config and rejected
  missing, changed, additional or path-escaping inputs and non-canonical/unknown
  seed directories.

## Suite, archive and evidence controls

- Full suite: `160 passed, 4 skipped` on the source commit. Skips were three
  explicit CUDA-hardware skips and one Windows symlink-creation skip.
- Final release-focused tests: `6 passed, 1 skipped`; the skipped adversarial
  symlink test is covered by fail-closed production checks and platform-neutral
  path/member tests.
- Git, source, wheel, sdist and offline archives contain MIT license metadata and
  no detected personal name/path, secret signature, checkpoint, embedding, raw
  data array or archive traversal member. The two immutable historical path files
  are absent from both Git-generated and curated source archives.
- Stage 09 remains `HOLD` with final QA `FAIL`; the recorded original/v2 hashes
  and Stage 09 QA report were not changed.

This is engineering reproducibility evidence only. It is not a formal study,
final-held-out evaluation, transfer result, CUDA validation or model-quality claim.
