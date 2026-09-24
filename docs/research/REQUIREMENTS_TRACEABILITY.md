# Requirements Traceability

| ID | Requirement | Registered verification and budget | Evidence stage | Claim boundary | Status |
|---|---|---|---:|---|---|
| R-01 | One checkpoint handles variable channel counts. | Shape tests plus deterministic nested unseen/nearest-seen views; paired relative domain-macro Smooth L1 degradation; interpolation/extrapolation separate; 3/5 paired seeds where comparative. | 0, 3, 6, 9 | Supported paired-view range and admitted public domains only; unpaired datasets are descriptive. | partial implementation; 미검증 at corpus scale |
| R-02 | Global representation is channel-order invariant. | Deterministic paired permutations; `1-cosine` primary and relative L2 diagnostic; Stage 03 threshold calibration. | 3, 9 | Global representation only; numerical pass rule pending Stage 03. | unit-tested; formal evaluator pending |
| R-03 | Metadata is optional. | Signal-only runs using frozen manifests and the common domain-macro protocol. | 0, 6, 9 | Optional metadata support, not equivalence of metadata-rich and signal-only quality. | implemented; broader validation pending |
| R-04 | Missing channels are supported and trained for. | Leakage tests plus paired 0/10/30/50% dropout degradation; matched steps/exposure. | 2, 3, 9 | Registered channel-removal corruption only. | pending |
| R-05 | Fly topology effect is isolated. | Primary paired domain-macro Smooth L1 (`beta=1.0`) versus both rewired and random; single-factor study; ±5% parameters; matched optimizer steps, exposure, tokenizer, router, and backbone capacity; five formal seeds. | 4, 5, 9 | Registered controls and budgets only; secondary outcomes cannot substitute for the primary topology endpoint. | pending |
| R-06 | Training runs on CPU and CUDA. | Device-specific backward/checkpoint tests with recorded hardware and environment. | 0, future hardware gate | CPU evidence does not imply CUDA behavior. | CPU recorded; CUDA pending |
| R-07 | Training is possible in a closed network. | No-network pipeline and final offline transfer verification with hashes. | 0, 10 | Recorded bundle and dependency set only. | MVP recorded; release verification pending |
| R-08 | Semiconductor adaptation follows public-data validation. | User stage gate after the public-data v0.1 evidence package. | after 10 | No semiconductor suitability or transfer claim before that gate. | deferred by design |
