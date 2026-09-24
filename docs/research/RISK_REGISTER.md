# FlyTS Risk Register

| ID | Risk | Impact | Current control | Status |
|---|---|---|---|---|
| RK-01 | Hidden target leaks through normalization or context. | invalid self-supervised results | visible-only statistics and explicit QA tests | active |
| RK-02 | Source ranges or groups leak across splits. | inflated downstream evidence | split-before-windowing, manifest ranges, QA | active |
| RK-03 | Topology comparison changes multiple factors. | false Fly-topology conclusion | matched front-end/budget protocol | active |
| RK-04 | Dataset rights or schema are misunderstood. | unusable corpus or invalid semantics | source notices, checksums, data review | active |
| RK-05 | Agent context drift or notebook staleness. | inconsistent implementation | concise CURRENT_STATE validation | active |
| RK-06 | Excess delegation consumes tokens without evidence gain. | budget exhaustion | activation matrix, delegation gate, stage budget | active |
| RK-07 | CUDA behavior is claimed without hardware validation. | misleading portability claim | explicit pending status and device tests | active |
| RK-08 | Final held-out or test evidence influences model, evaluator, or threshold selection. | invalid final evidence and selection leakage | sealed Stage 06 domain registry, Stage 09 one-time opening, freeze manifest, QA audit | active |
| RK-09 | Numerical thresholds or uncertainty rules are chosen after seeing results. | metric shopping and optimistic pass/fail claims | Stage 03 development-only calibration and hash freeze before formal comparison | active |
| RK-10 | Frozen-probe or source-transfer tasks use incompatible label ontologies. | uninterpretable transfer claim | target-local probes by default; source transfer requires pre-result ontology evidence | active |
| RK-11 | Topology comparisons change tokenizer, router, backbone, or graph controls simultaneously. | false topology attribution | single-factor matrix, graph statistics, ±5% parameters, matched steps/exposure | active |
| RK-12 | FLOPs, wall time, or sparse-kernel efficiency are treated as interchangeable compute budgets. | unfair comparison or misleading efficiency claim | optimizer steps are primary; report estimator limits, controlled time, memory, and latency separately | active |
