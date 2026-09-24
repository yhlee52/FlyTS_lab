# Stage 01 Result — Research and Experiment Protocol

Status: review

Date: 2026-09-24
Base commit: `ad9655f76bd140776514a4029ccc77ccf779b20f`

## Conclusion

Stage 01 produced an approved, leakage-resistant, budget-matched, claim-to-evidence protocol for Stages 2–10 without changing code, configuration, data, manifests, model behavior, or training. All scientific hypotheses remain `미검증`; this stage defines how later evidence may support, fail to support, harm, revisit, or stop a claim.

## Acceptance evidence

| Criterion | Result | Evidence |
|---|---|---|
| Fourteen decision areas | Pass | DEC-007, project consensus, and experiment protocol; numerical calibration explicitly assigned to Stage 03. |
| H/R traceability | Pass | H-01–H-04 and R-01–R-08 record metrics, controls, stages, and claim boundaries. |
| Split and leakage controls | Pass | Split-before-windowing, train-only preprocessing, development calibration, Stage 06 final-domain seal, Stage 09 one-time final test. |
| Selection and repetition | Pass | Domain-macro Smooth L1 `beta=1.0`; 1/3/5 paired repetitions. |
| Matched budgets | Pass | ±5% trainable parameters; optimizer steps, exposure, batch, context, optimizer, and schedule controls. |
| Foundation metrics | Pass | Reconstruction, permutation, dropout, unseen count, controlled frozen probes, transfer, and efficiency contracts. |
| Factor isolation | Pass | Separate topology, tokenizer, router, and backbone single-factor contrasts. |
| Negative results | Pass | Support/no-support/harm/revisit/stop with one retained diagnostic rerun. |
| Scope integrity | Pass | Documentation changes only; no implementation, data, config, training, or performance claim. |
| Independent QA and validators | Pass | Final QA `PASS`; notebook, governance, and diff validation pass. |

## Frozen protocol summary

- Two-tier domain isolation; final domains selected at Stage 06 before performance inspection and sealed until Stage 09.
- Validation-only domain-macro Smooth L1 (`beta=1.0`) selection; final test cannot tune or rerank.
- One smoke, three development, and five formal paired seeds.
- ±5% trainable-parameter matching and optimizer-step primary compute matching with fixed exposure controls.
- Paired permutation, dropout, unseen/seen count, probe-control, and topology endpoints with equal-domain aggregation.
- Stage 03 owns numerical thresholds, interval method, numerical guards, and evaluator fixtures using development evidence only.
- Stage 09 first opens final held-out/test evidence; Stage 10 packages it without retuning.

## QA and limitations

Independent QA initially found four incomplete metric contracts and issued `FAIL`. The user approved the recommended remediation; QA used its one follow-up to verify the completed contracts and issued `PASS`.

Stage 03 must still calibrate numerical thresholds, uncertainty rules, permutation/count fixtures, and numerical guards. Stage 06 must admit eligible datasets and freeze domain roles. Runtime leakage prevention, model performance, transfer, topology benefit, CUDA support, offline release verification, and semiconductor adaptation remain unverified.

## Artifacts

- Charter: `docs/research/stages/stage-01/CHARTER.md`
- Project consensus: `docs/PROJECT_CONSENSUS.md`
- Experiment protocol: `docs/EXPERIMENT_PROTOCOL.md`
- Independent QA: `docs/research/stages/stage-01/QA_REPORT.md`
- Decision authority: `docs/research/DECISION_LOG.md` DEC-007
- Traceability and risks: `docs/research/HYPOTHESES.md`, `REQUIREMENTS_TRACEABILITY.md`, and `RISK_REGISTER.md`

No PR is merged and Stage 02 has not begun.
