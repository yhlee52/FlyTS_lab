# FlyTS Hypothesis Register

| ID | Hypothesis | Protocol mapping | Historical evidence stage | Claim boundary | Status |
|---|---|---|---:|---|---|
| H-01 | A channel-agnostic front-end can encode variable channel counts with channel-order-invariant global representations. | Development/final held-out domains; permutation `1-cosine`; paired relative domain-macro Huber degradation against nearest seen-count nested views, with interpolation and extrapolation separate; 3 development and 5 formal paired seeds. | 3, 6, 9 | Representation invariance and count generalization only; not downstream quality or universal domain transfer. | HOLD — numerical freeze/formal/final inference not run; no support result |
| H-02 | Channel masking/dropout improves robustness to missing sensors without unacceptable representation collapse. | Matched masking pretraining; paired 0/10/30/50% dropout; per-rate relative degradation; domain-macro primary; identical step/exposure budget. | 2, 3, 9 | Robustness under registered corruption and datasets only; no physical sensor-failure guarantee. | HOLD — numerical freeze/formal/final inference not run; no support result |
| H-03 | Fly-like sparse recurrent topology provides useful inductive bias beyond matched rewired and random topology. | Primary paired domain-macro Smooth L1 (`beta=1.0`) differences versus both rewired and random; single-factor controls; tokenizer/router/backbone fixed; ±5% parameters; matched optimizer steps/exposure; five formal paired seeds. | 4, 5, 9 | Benefit, null, or harm under the registered controls only; secondary robustness/probe results cannot rescue a failed primary endpoint, and a null result does not refute the front-end. | HOLD — numerical freeze/formal/final inference not run; no support result |
| H-04 | Public multi-domain pretraining produces reusable representations for held-out domains. | Two-tier isolation; target-local frozen probes using macro-F1 or train-standardized RMSE against paired random-init and visible-statistics controls; separately PI-authorized Stage 09 one-time final test; optional source transfer only with compatible label ontology. | 6, 9 | Target-local representation transfer by task family; not a pooled task-agnostic, zero-shot, universal, or semiconductor-transfer claim. | HOLD — HARTH unadmitted; not tested |

Update evidence status only from recorded experiments, not architectural intuition.

## Prospective Phase 02 responsibility (DEC-072)

The evidence-stage numbers above describe the historical Stage 01/09 protocol and
Stage 09's closed `HOLD`, not completed formal outcomes or a Phase 02 run plan.
The old numerical candidates, five-seed/60-run proposal and H-04 exclusion are
not automatically transferred to a future protocol v3.

| Hypothesis | Adequacy and protocol | Execution, decision and claim gate |
|---|---|---|
| H-01 | Stage 12 Data audits independent units, count coverage and paired views; Stage 13 Experiment freezes permutation/count rules; Stage 14 QA checks masks and leakage. | Stages 15–16 Experiment records valid matched outcomes; Stage 18 final evidence needs Stage 17 PI unseal; Stage 19 permits only tested-domain/count claims. |
| H-02 | Stage 12 Data audits missingness and paired corruption coverage; Stage 13 Experiment freezes robustness and clean-harm rules; Stage 14 QA checks target/reference separation. | Stages 15–16 Experiment records matched masking outcomes; Stage 19 limits any claim to registered corruption. |
| H-03 | Stage 12 Data audits domain adequacy; Stage 13 Experiment freezes both primary contrasts and matched budgets; Stage 14 QA checks topology and single-factor controls. | Stages 15–16 Experiment records both primary comparisons; Stage 19 allows Q3 only after Q2 and support against both controls. |
| H-04 | Stage 12 Data audits an eligible labeled target and requests separate PI source/role/split approval; Stage 13 Experiment freezes general task-family probe and control rules. | Stage 17 Data/Experiment/QA binds an approved target-specific packet and seeks a separate PI gate; Stage 18 Experiment/QA opens approved test once; Stage 19 records bounded task-family evidence or `not tested`. |

No row authorizes dataset admission, training, test access or a positive result.
