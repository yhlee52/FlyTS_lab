# Stage 07 Result — Conventional Backbone Engineering

Status: **closed — independent QA PASS; PI result GO**

PR: [#13](https://github.com/yhlee52/FlyTS_lab/pull/13) — merged into `main`

Integration note: PR #13 was subsequently merged into `main` at
`34b83c29d8a5588158d1e4abe420bfc8cbdf5e68` on 2026-09-27. This does not
alter the Stage 07 evidence, independent QA verdict or bounded claim policy.

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

Post-QA Linux CI showed that seeded tensor value hashes vary across operating
systems even though paired shared tensors remain bitwise equal within each run.
The stable report therefore records the actual equality result and a hash of its
name/shape/dtype/equality transcript, not a platform-specific tensor-value hash.
Both Draft PR #13 Linux `pytest` checks pass with this cross-OS contract.

CUDA, performance, transfer, robustness pass/fail, foundation quality and backbone
or topology superiority remain `미검증`. Draft PR creation is authorized; merge and
Stage 08 remain unauthorized.

## PI result decision

The PI issued `GO` on 2026-09-27 after reviewing the implementation, parameter
contract, independent QA, cross-platform report evidence, limitations and passing
Draft PR checks. Stage 07 is closed within this bounded engineering scope. Draft PR
#13 merge, Stage 08, real-data training and every performance claim remain separately
unauthorized.
