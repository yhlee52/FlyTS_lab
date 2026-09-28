# FlyTS-Mini v0.1 Research Preview — Closeout Report

Status: Stage 10 release candidate; M8/M9 evidence pending

## Conclusion

FlyTS has a reproducible engineering MVP and public-data operational pipeline for
variable-channel multivariate time series. Formal comparison and final-held-out
evaluation were not performed, so Fly topology superiority, masking benefit,
foundation representation quality and transfer capability cannot be judged.
The next research cycle must improve independent data/evaluation units and freeze
a new protocol before formal work resumes.

This preview is not a validated foundation model or production model. It includes
no pretrained checkpoint.

## Engineering completion

Recorded engineering capabilities include:

- variable-length and variable-channel `[B,T,C]` handling;
- shared patch tokenization, slot routing and interchangeable recurrent backbones;
- visible-only normalization and distinct missing/padding/training masks;
- fly-like, degree-preserving rewired and random sparse topology modules;
- dense-leaky and GRU engineering baselines with matched-parameter tooling;
- public source locking, split-before-windowing and domain-role enforcement;
- CPU training, validation-only selection, checkpoint save/load/resume, embedding
  export and development evaluator paths;
- offline corpus pack/unpack and transfer-bundle integrity verification;
- stage-specific tests, provenance and independent engineering QA through Stage 08.

Stage 10 still requires clean-room and independent release QA before these paths
are accepted as release-supported for the exact candidate bytes.

## Scientific/model completion

Scientific/model completion was not achieved:

- Stage 09 ended at `HOLD`; final reporter QA is `FAIL`.
- H-01, H-02 and H-03 have no formal result.
- H-04 is `not tested` because HARTH was not admitted.
- Numerical guards, effects and uncertainty rules were not frozen.
- The 60-run protocol-v2 matrix was not frozen or executed.
- Electricity final-held-out model evidence was not opened.
- No checkpoint was selected for publication.
- CUDA and semiconductor behavior were not validated.

## Evidence carried forward

Stage 08's four core arms each completed 400 CPU steps and 3,200 exposures in one
seed with independent QA `PASS`. That result demonstrates the bounded operational
pipeline only. Its individual losses do not identify a winner, justify a mean or
significance statement, select a checkpoint or fix a future budget.

Stage 09 preserves useful readiness tooling, graph-cache/unseal controls, one-row
synthetic rehearsal evidence, development-only calibration and HARTH non-admission
evidence. Its 60-row proposal passed consistency QA only. Historical bounded
sub-review `PASS` results do not override the final Stage 09 `HOLD` and QA `FAIL`.

The failed `REPORT-v2` remediation remains historical evidence at recorded hashes.
Stage 10 may validate a new prospective declared-input reporter contract but does
not regenerate or relabel the Stage 09 result.

## Release composition

The candidate consists of source, `flyts 0.2.0` wheel/sdist, exact supported
configs, documentation, manifest/checksums, a synthetic fixture and a small
checkpoint-free offline verification bundle. The research version and Python
package version remain separate axes.

The candidate excludes raw public/company data, Stage 08/09 raw outputs, all
checkpoints and embeddings, HARTH artifacts, Electricity model outputs, private
paths or metadata, unsupported binaries and target-unspecified dependency
wheelhouses. It is not published to PyPI.

## Dataset and rights boundary

Appliances and Beijing remain pretraining domains, Bike remains development-only
and Electricity remains final-held-out. Raw bytes are not distributed. Official
source references, stated licenses, observed hashes and preparation instructions
are provided for reproducibility; they are not legal guarantees.

HAR remains excluded due to conflicting rights statements. HARTH remains
unadmitted because the sole fixed test split lacks one official class, one
subject's cadence semantics conflict and its archive lacks a bundled notice.

## Hardware boundary

The recorded workflow is CPU float32. CUDA paths are not validated on hardware;
CUDA skips must be reported rather than treated as success. The offline candidate
does not contain a dependency wheelhouse, so target dependencies must be approved
and supplied separately.

## Decision outcome

Among the original development-plan conclusions, current evidence supports:

> Data and evaluation are insufficient, so limited additional validation is
> required.

It does not support expanding the model/corpus based on topology benefit, claiming
that the channel-agnostic front-end is scientifically validated, or rejecting the
backbone hypothesis from an unexecuted formal study.

## Remaining release gates

1. Generate and verify the commit-bound M5/M6 manifest and candidate artifacts.
2. Complete security/rights/hygiene and clean-room QA.
3. Obtain independent Stage 10 QA.
4. Obtain M10A PI approval before push/Draft PR.
5. After user merge and tree verification, obtain M10B PI approval before tag or
   GitHub prerelease creation.
