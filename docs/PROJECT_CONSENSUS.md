# FlyTS Project Consensus

Status: approved for Stage 01 protocol work on 2026-09-24

## Mission and research question

FlyTS is a channel-agnostic multivariate time-series foundation encoder. The first complete target is the public-data `FlyTS-Mini v0.1` evidence package; semiconductor adaptation remains deferred until after its Stage 10 gate.

The scientific question is whether public multi-domain pretraining can produce reusable representations across variable channel counts and orders, and whether a fly-like sparse recurrent topology adds value beyond matched non-topological or controlled-topology alternatives.

The active hypotheses are H-01 through H-04 in `docs/research/HYPOTHESES.md`. They remain `미검증` until their registered evidence is recorded; architectural intuition, Stage 00 smoke results, and Stage 01 protocol agreement are not evidence of model quality.

## Decision authority and canonical protocol

- The user is the final authority for stage scope, research questions, splits, metrics, budgets, acceptance criteria, PR merge, and stage advancement.
- `docs/research/DECISION_LOG.md` DEC-007 records the approved Stage 01 choices.
- `docs/EXPERIMENT_PROTOCOL.md` is the operational protocol. If it conflicts with the development plan, hypothesis register, or a run configuration, work stops until the documents are reconciled through the user gate.
- Numerical performance thresholds are not set in Stage 01. Stage 03 calibrates and freezes them using development evidence without final-test access.

## Domain and split contract

- Split source records, groups, and time ranges before window creation. Preserve purge gaps and prove that train, validation, and test ranges do not overlap.
- Fit normalization, preprocessing statistics, and any learned data transform from training-visible values only. Hidden targets, validation, development held-out, and final held-out data cannot influence those statistics.
- Development held-out domains may be used for evaluator design and Stage 03 calibration through leave-one-domain-out analysis.
- At the Stage 06 corpus freeze, assign final held-out domains using eligibility, rights, schema, and coverage criteria before performance inspection. Seal them until Stage 09.
- Validation selects checkpoints and settings. Stage 09 opens the frozen final test once after models, seeds, evaluator, thresholds, probes, and protocol are frozen. Stage 10 packages the recorded evidence and does not retune from it.

## Selection, repetition, and matched budgets

- Primary checkpoint selection is validation-only domain-macro masked Huber loss, aggregated from valid masked targets to records, domains, and then equal-weight domains.
- Masked Huber is the PyTorch Smooth L1 definition with `beta=1.0` after train-only normalization.
- Use one deterministic seed for smoke checks, three paired seeds for development and ablation, and five paired seeds for the Stage 09 formal study. Report every seed and domain result.
- Match each comparison arm within ±5% of a common trainable-parameter target. Report actual counts; an arm outside tolerance is unmatched and cannot support a superiority claim.
- Optimizer steps are the primary compute match. Also hold batch, context, data exposure, mask schedule, optimizer, and learning-rate schedule fixed where the comparison intends only one factor to vary.
- FLOPs, wall time, peak memory, and latency are reported efficiency evidence, not model-selection criteria.

## Evaluation and factor isolation

The common evaluation family is masked reconstruction, channel permutation distance, 10/30/50% channel-dropout degradation, channel-count interpolation and extrapolation, frozen linear probes, held-out-domain transfer, and controlled efficiency measurement. Per-domain and domain-macro results are primary; micro and worst-domain results are diagnostics.

Topology, tokenizer, router, and backbone are separate experimental factors. A topology claim requires tokenizer, router, backbone capacity, data, optimization, exposure, and budget controls to remain fixed. Router, tokenizer, or backbone ablations hold topology fixed. A contrast that changes more than one factor cannot attribute the outcome to topology.

H-03's primary topology endpoint is the paired difference in final domain-macro masked Huber between fly-like and each of the rewired and random controls. Both registered contrasts must satisfy the Stage 03-frozen effect and uncertainty rules for a topology-support claim. Robustness, probes, transfer, and efficiency are secondary outcomes and cannot rescue a failed primary topology endpoint.

Channel-count interpolation and extrapolation use deterministic nested channel views from the same source record. The primary outcome is relative domain-macro Huber degradation against the nearest seen-count paired view on shared targets. Target-local frozen probes use macro-F1 for classification and train-standardized RMSE for regression, compared with paired random-init encoder and visible-statistics controls. Classification and regression families remain separate rather than being combined into a task-agnostic score.

## Outcome and claim policy

- `support`: the prespecified primary evidence meets the Stage 03-frozen threshold and uncertainty rule without a guardrail or protocol failure.
- `no-support`: the valid result is null, inconclusive, or below the prespecified support rule.
- `harm`: the valid paired evidence shows a credible adverse effect under the frozen rule.
- `revisit`: a prespecified instrumentation, data-integrity, or protocol defect permits one diagnostic rerun. Preserve both original and rerun evidence.
- `stop`: the defect remains unresolved, comparison fairness cannot be achieved, or the diagnostic rerun leaves the hypothesis unsupported or harmful under the approved decision rule.

A negative result supports only a bounded statement such as “no evidence of benefit under this matched protocol.” It does not prove that an architecture is universally ineffective. A null topology result does not refute the channel-agnostic front-end.

## Stage 02–10 handoff

| Stage | Protocol handoff |
|---:|---|
| 2 | Implement masking and dropout leakage controls; no performance gate. |
| 3 | Implement the common evaluator and calibrate counts, interval method, and numerical thresholds on development evidence only. |
| 4 | Modularize topology without intended behavior change. |
| 5 | Compare fly-like, degree-preserving rewired, and random sparse controls under the frozen matched protocol. |
| 6 | Freeze the rights- and schema-audited public corpus and assign domain roles before performance inspection. |
| 7 | Add dense recurrent and GRU baselines with the shared tokenizer/router and matched budgets. |
| 8 | Run a small pipeline pilot to find execution defects; make no formal performance claim. |
| 9 | Run the five-seed formal study and open final held-out/test evidence once. |
| 10 | Package the reproducible evidence, including negative or inconclusive conclusions, for the user gate. |

## Persistent limitations

CUDA execution, foundation-model quality, held-out transfer, topology benefit, corpus-scale channel-count generalization, and semiconductor adaptation remain unverified. Source rights, schema, time semantics, label ontology, split integrity, and checksums remain dataset-admission gates.
