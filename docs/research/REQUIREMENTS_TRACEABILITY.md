# Requirements Traceability

| ID | Requirement | Planned verification | Stage | Status |
|---|---|---|---:|---|
| R-01 | One checkpoint handles variable channel counts. | shape tests and multi-dataset evaluation | 0, 3, 6 | partial implementation; 미검증 at corpus scale |
| R-02 | Global representation is channel-order invariant. | permutation distance and regression test | 3 | unit-tested; formal evaluator pending |
| R-03 | Metadata is optional. | signal-only corpus runs | 0, 6 | implemented; broader validation pending |
| R-04 | Missing channels are supported and trained for. | channel masking/dropout tests and evaluation | 2, 3 | pending |
| R-05 | Fly topology effect is isolated. | fly-like vs rewired vs random matched study | 4, 5, 9 | pending |
| R-06 | Training runs on CPU and CUDA. | device-specific backward/checkpoint tests | 0 | CPU recorded; CUDA pending |
| R-07 | Training is possible in a closed network. | no-network pipeline and transfer verification | 0, 10 | MVP recorded; release verification pending |
| R-08 | Semiconductor adaptation follows public-data validation. | stage-gate decision after v0.1 | after 10 | deferred by design |
