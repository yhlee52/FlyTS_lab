# Stage 07 Result — Conventional Backbone Engineering

Status: **review — independent QA PASS; PI result pending**

Draft PR: [#13](https://github.com/yhlee52/FlyTS_lab/pull/13) — open, unmerged

The approved engineering question is satisfied. Fly sparse, dense-leaky and GRU
share one tokenizer, Set Router, masking, contextual head, decoder and reconstruction
path behind a common routed-slot interface. Existing Fly format-v1 checkpoints and
`graph.*` state remain compatible. No real-data or performance comparison was run.

Fly has 68,760 trainable parameters; dense-leaky selects `H=98` and 68,530;
GRU selects `H=43` and 68,853. All arms are within five percent, share 27,208
trainable front-end/head parameters and pass fixed-mask finite-gradient/update,
padding, adapter and bitwise two-step-resume checks.

Initial QA `FAIL` found newline-normalized config provenance and incomplete source
binding. DEC-025 remediation writes and checks exact bytes, binds 19 sources and
rejects CRLF drift. Final QA is `PASS`: focused 64 passed/2 CUDA skips, full 97
passed/3 CUDA skips, report/validators/diff pass.

CUDA, performance, transfer, robustness pass/fail, foundation quality and backbone
or topology superiority remain `미검증`. Draft PR creation is authorized; merge and
Stage 08 remain unauthorized. PI result decision is pending.
