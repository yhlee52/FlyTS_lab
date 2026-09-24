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
