# FlyTS Experiment Protocol

Version: Stage 01 approved protocol, 2026-09-24

## 1. Protocol freeze and provenance

Every reported run records the Git commit, complete config, dataset manifest and hashes, domain-role registry, seed, parameter count, optimizer steps, sample exposure, environment, device, primary and diagnostic metrics, timing, memory, and artifact paths.

Before a formal Stage 09 run, freeze and hash the model definitions, dataset/domain roles, split manifests, seeds, evaluator version, Stage 03 thresholds and interval method, probe settings, budget target, and run configs. Any post-freeze change creates a new protocol version and requires the applicable user gate. Final-test output never tunes, filters, reranks, or selects a run.

## 2. Domain roles and split safety

### 2.1 Domain roles

- `pretrain`: may contribute training and validation records.
- `development-held-out`: excluded from the relevant pretraining fold and usable for LODO evaluator development and Stage 03 calibration.
- `final-held-out`: selected at the Stage 06 corpus freeze before performance inspection, excluded from pretraining and evaluator calibration, and sealed until Stage 09.

The Stage 06 domain-role registry records the assignment date, eligibility, source rights, schema, sampling semantics, channel count, task/label availability, and manifest hash. A domain cannot change role after its performance is inspected without a new user-approved protocol version.

### 2.2 Within-domain splits

Split source records, entities/groups, and chronological ranges before windowing. Apply purge gaps where adjacent windows could share target or contextual information. No source group, raw range, or derived window may cross train, validation, and test roles.

Fit normalization and other preprocessing statistics from training-visible values only. Originally missing values, padding, masked targets, validation, and held-out data are excluded. Save the fitted state and its training manifest hash.

### 2.3 Selection and final test

Training data fits model parameters. Validation data selects checkpoints and allowed settings. Development-held-out data supports protocol development and Stage 03 calibration but cannot serve as final evidence. Stage 09 opens final-held-out/test evidence once after the protocol freeze. Stage 10 republishes the fixed evidence without retuning.

## 3. Primary model selection

For record `r` in domain `d`, let `T_r` be positions that were originally observed, are valid rather than padding, and were hidden by the evaluation mask. The record loss is

```text
L_record(r) = mean_{i in T_r} Huber(y_i, y_hat_i)
L_domain(d) = mean_{r in d} L_record(r)
L_select = mean_{d in validation domains} L_domain(d)
```

`L_select` is the sole primary checkpoint/model-selection metric and lower is better. Report per-domain, micro, and worst-domain losses as diagnostics; they cannot override the primary ranking. An empty `T_r` is a protocol error, not a zero-loss record.

Huber is fixed to PyTorch Smooth L1 loss with transition parameter `beta=1.0`, applied after normalization fitted only from training-visible values. Reduction occurs only over `T_r`; Stage 03 does not retune `beta`.

## 4. Seeds, repetitions, and uncertainty

- Smoke and pipeline checks: one deterministic seed; no performance claim.
- Development and ablation: three paired seeds shared by all comparison arms.
- Stage 09 formal study: five paired seeds shared by all comparison arms.

Retain every record-, domain-, seed-, and arm-level result. Report individual values, mean, standard deviation, and paired arm differences. Stage 03 selects and freezes the uncertainty-interval estimator using null/development evidence; seed variation alone does not establish generalization across domains.

## 5. Parameter and compute matching

For a matched comparison, declare one trainable-parameter target before training. Every arm must fall within ±5% of that target. Report the target, actual count, absolute difference, and percentage difference. Out-of-tolerance arms are unmatched and cannot support comparative superiority claims.

Optimizer steps are the primary compute budget. Hold batch size, context length, number of train/validation examples exposed, masking schedule, optimizer, learning-rate schedule, precision, checkpoint policy, and data order rules fixed unless the factor under study logically requires one of them to change. Any required exception is preregistered and reported.

Report estimated FLOPs with the accounting method and limitations, but do not use unreliable sparse/recurrent FLOPs as the primary match. Record end-to-end and steady-state time, peak memory, and latency under the measurement rules in Section 7.

## 6. Foundation evaluation contracts

Position-wise reconstruction metrics use the aggregation order valid positions → record → equal-weight records within domain → equal-weight domains. Representation distances are first computed per record and then aggregated through equal-weight records and domains. Probe metrics follow their task-specific within-domain rule in Section 6.5. Report per-domain and applicable micro diagnostics alongside each domain macro.

### 6.1 Masked reconstruction

Evaluate only valid, originally observed positions hidden by the evaluator. Use paired evaluator masks across model arms. Primary loss is domain-macro Huber; MAE or other losses are diagnostic unless a later user-approved protocol changes the primary metric.

### 6.2 Channel permutation distance

For global representation `Z` and a deterministic non-identity channel permutation `P`:

```text
D_perm = 1 - cosine(normalize(Z(X)), normalize(Z(P(X))))
```

Report relative L2 representation distance as a diagnostic. Stage 03 freezes the deterministic permutation set, repeat count, numerical floor, and pass/fail threshold from no-op and order-sensitive controls without final-test access.

### 6.3 Channel-dropout robustness

Evaluate paired deterministic channel masks at 0%, 10%, 30%, and 50%, always retaining at least one channel. For a lower-is-better loss:

```text
degradation(p) = (metric_p - metric_0) / abs(metric_0)
```

For higher-is-better scores, reverse the numerator sign so positive values always mean degradation. If the baseline magnitude is below the Stage 03-frozen numerical guard, report absolute change and mark relative degradation undefined. Each rate is primary evidence; an area-under-curve summary is diagnostic and cannot hide a severe 50% failure.

### 6.4 Unseen channel counts

Derive the set of channel counts actually observed during training from the frozen manifests. Report separately:

- interpolation: withheld counts inside the observed minimum/maximum range;
- extrapolation: counts outside that range but inside the evaluator's supported range.

For an unseen count `c_u`, choose the nearest seen count `c_s`; ties choose the smaller count. Build both views from the same source record using a deterministic manifest-hashed channel ordering and nested subsets. Evaluate the same valid masked targets on channels shared by both views. Let `L_u` and `L_s` be their domain-macro Smooth L1 losses:

```text
D_count(c_u) = (L_u - L_s) / abs(L_s)
```

Positive values mean degradation and lower is better. If `L_s` is below the Stage 03-frozen numerical guard, report the absolute paired difference and mark the relative result undefined. A dataset without valid paired nested views supplies descriptive evidence only and cannot satisfy the primary channel-count claim.

Do not pool interpolation and extrapolation into one pass/fail result. Stage 03 freezes the deterministic channel-view fixtures, supported counts, numerical guard, thresholds, and uncertainty rule; Stage 06/09 adds corpus evidence where eligible domains permit it.

### 6.5 Frozen probes and held-out transfer

The encoder is frozen. A target-local linear probe fits only target-domain training labels, selects regularization and stopping from target validation labels, and opens target test once. The target domain is absent from encoder pretraining and evaluator calibration when used as final held-out evidence.

Primary task metrics and directions are:

- classification: macro-F1, higher is better;
- regression: RMSE after standardizing the target with target-train mean and standard deviation only, lower is better.

Use two paired controls with identical target splits and probe-selection rules: a frozen random-initialized encoder of the same architecture and a visible-statistics feature baseline. The statistics baseline concatenates, in the target manifest's channel order, per-channel observed mean, standard deviation, minimum, maximum, last observed value, and missingness fraction computed from the input context; any imputation state is fitted on target train only.

For classification, the primary per-domain probe effect is

```text
Delta_probe = F1_pretrained - max(F1_random_init, F1_visible_stats)
```

For regression, it is

```text
Delta_probe = min(RMSE_random_init, RMSE_visible_stats) - RMSE_pretrained
```

Positive values favor the pretrained representation. Aggregate domains equally within classification and regression families, but do not pool the two task families into one scalar. Stage 03 freezes the effect/uncertainty rule; H-04 support requires the frozen rule in every eligible reported task family and no family-level harm.

Within each classification domain, compute macro-F1 from all target-test predictions by giving each registered class equal weight. Within each regression domain, compute RMSE over all target-test predictions in train-standardized target units. Only after these within-domain metrics and paired control effects are computed are domains given equal weight within their task family.

Source-trained cross-domain probes are optional diagnostics only when label ontologies and target definitions are documented as compatible before results are viewed. Otherwise do not compute or imply zero-shot transfer.

## 7. Efficiency measurement

Record hardware, OS, Python/PyTorch, device, thread count, dtype, batch, context, channel count, and model/config hash. Use the same environment and benchmark inputs for compared arms.

- Training: report end-to-end time and steady-state time per optimizer step, excluding separately reported setup/data-preparation time.
- Memory: report peak process RSS on CPU and, when actual CUDA hardware is available, peak allocated/reserved CUDA memory with synchronization.
- Inference: after 10 untimed warm-up iterations, report median and p95 over 100 synchronized timed iterations, both per batch and per sample.
- Complexity: report trainable parameters and estimated FLOPs with the estimator version and unsupported operations.

Efficiency evidence is never a substitute for the primary validation metric and does not authorize a CUDA claim without hardware validation.

## 8. Single-factor attribution

| Claim factor | Must vary | Must remain fixed |
|---|---|---|
| Topology | fly-like, degree-preserving rewired, or random sparse graph | tokenizer, router, backbone width, data, schedule, steps, exposure, parameter tolerance |
| Tokenizer | tokenizer only | topology, router, backbone, data, schedule, budgets |
| Router | router only | tokenizer, topology, backbone, data, schedule, budgets |
| Backbone | backbone family only | tokenizer, router, data, schedule, exposure, agreed budgets |

Record graph nodes, edges, sparsity, in/out degree, reciprocity, modularity, populations, and generator seed. Match the graph properties intended by each control; do not call a random graph “degree matched” unless measured statistics satisfy the frozen control rule. A multi-factor contrast may be reported descriptively but cannot attribute an effect to topology.

H-03's primary Stage 09 topology endpoints are paired differences in final domain-macro masked Huber:

```text
Delta_rewired = L_fly_like - L_rewired
Delta_random = L_fly_like - L_random
```

Negative values favor fly-like topology. A topology-support claim requires both contrasts to meet the Stage 03-frozen effect and uncertainty rules with no protocol or guardrail failure. Robustness, frozen-probe, transfer, and efficiency results are secondary; they may support bounded secondary claims but cannot rescue a no-support primary topology result.

## 9. Outcome, diagnostic rerun, and stop rules

- `support`: valid prespecified primary evidence meets the Stage 03-frozen effect and uncertainty rules without a protocol or guardrail failure.
- `no-support`: valid evidence is null, inconclusive, or below the support rule.
- `harm`: valid paired evidence meets the frozen adverse-effect rule.
- `revisit`: a preregistered instrumentation, data-integrity, or protocol defect justifies one diagnostic rerun. Retain and report both results.
- `stop`: the defect remains unresolved, fairness cannot be restored, or the one diagnostic rerun still yields no-support/harm for the claim being pursued.

Do not add seeds, domains, metrics, thresholds, or reruns after viewing results unless the user approves a new protocol version. Negative claims remain bounded to the tested data, budget, and comparison arms.

## 10. Stage handoffs and prohibited interpretation

- Stage 02 implements masking/dropout and leakage tests without a performance gate.
- Stage 03 implements the common evaluator and freezes calibration-owned constants without final-test access.
- Stages 04–07 implement factor interfaces and comparison arms under this protocol.
- Stage 08 is an operational pilot, not formal performance evidence.
- Stage 09 performs the five-seed formal study and first final-test opening.
- Stage 10 packages the fixed evidence and limitations.

Until recorded evidence exists, do not claim foundation-model quality, transfer, topology superiority, corpus-scale generalization, CUDA support, or semiconductor suitability.
