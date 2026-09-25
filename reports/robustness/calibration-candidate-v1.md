# Stage 03 calibration candidate — GO to defer freeze; HOLD additional scope

Manifest: `e538e9cbf761577740f43f6930ac4653834fdc00f9d0ee567b02b52e2d0d14eb`; split: `val`; seeds: `7/17/29`; 400 steps each.
User accepted the candidate evidence milestone. Threshold, numerical guard and uncertainty settings remain candidate; additional evidence needs separate approval.
Test and final-held-out were excluded. All values and options are candidate only.

| Metric | Arm | Mean domain macro | 95% candidate interval | Eligible domains / source records | Coverage |
|---|---|---:|---:|---|---|
| channel_count | extrapolation:1->4 | 0.0039871005 | [0.0002532108, 0.011209492] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| channel_count | extrapolation:3->4 | -0.00035894895 | [-0.0013562694, 0.00019431814] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| channel_count | interpolation:10->11 | 1.8983996e-05 | [-8.6356243e-05, 0.00023105873] | 2 / 13 (energy:1, environment:12) | limited_domain_or_record |
| channel_count | interpolation:12->11 | -4.3931538e-05 | [-9.9714336e-05, 3.6860003e-08] | 1 / 1 (energy:1) | single_domain_single_record |
| channel_count | interpolation:18->11 | -1.9691351e-05 | [-6.222382e-05, 1.9980755e-05] | 1 / 1 (energy:1) | single_domain_single_record |
| channel_count | interpolation:25->26 | 1.9880177e-05 | [1.562464e-05, 2.7564123e-05] | 1 / 1 (energy:1) | single_domain_single_record |
| channel_count | interpolation:5->4 | -0.0001175364 | [-0.00034589411, -9.2122689e-06] | 2 / 13 (energy:1, environment:12) | limited_domain_or_record |
| channel_count | interpolation:7->4 | -0.0003279056 | [-0.0008364681, -1.8536185e-05] | 2 / 13 (energy:1, environment:12) | limited_domain_or_record |
| dropout | 0% | 0 | [0, 0] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| dropout | 10% | -6.0350805e-05 | [-0.00031585745, 0.00010481353] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| dropout | 30% | 9.106571e-06 | [-0.00077999564, 0.00062726104] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| dropout | 50% | -0.00038069709 | [-0.0020401574, 0.00077340162] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| missing | block:10% | 0.0030016037 | [-0.001869683, 0.0091492633] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| missing | block:30% | -0.015590464 | [-0.031373861, 0.010080095] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| missing | block:50% | -0.013042061 | [-0.049459901, 0.081025925] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| missing | mcar:10% | -0.00058927518 | [-0.0024785596, 0.00051186465] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| missing | mcar:30% | -0.0041504884 | [-0.012822786, 0.0014577479] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| missing | mcar:50% | -0.0043838068 | [-0.016584072, 0.0070587162] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| padding | both | 2.452311e-08 | [2.0614639e-08, 3.090892e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| padding | channel | 7.2268863e-09 | [0, 2.1040504e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| padding | time | 2.4790868e-08 | [2.086292e-08, 3.1557897e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| permutation | identity | 0 | [0, 0] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| permutation | perm_0 | 1.9933445e-08 | [1.4152358e-08, 2.5459143e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| permutation | perm_1 | 1.9804858e-08 | [1.453331e-08, 2.4775045e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| permutation | perm_2 | 2.1585569e-08 | [1.6913393e-08, 2.7244135e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| permutation | perm_3 | 1.9484387e-08 | [1.3498131e-08, 2.5500433e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| permutation | perm_4 | 2.3588698e-08 | [1.935428e-08, 2.9179692e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| permutation | perm_5 | 1.9568651e-08 | [1.3795622e-08, 2.4971089e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| permutation | perm_6 | 2.0406049e-08 | [1.6081692e-08, 2.4150699e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| permutation | perm_7 | 2.2847715e-08 | [1.8217458e-08, 3.1348923e-08] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |
| reconstruction | baseline | 0.52159175 | [0.50990904, 0.54446983] | 3 / 14 (energy:1, environment:12, transport:1) | limited_domain_or_record |

## Controls and decision

Identity permutation: [0.0]; zero dropout: [0.0]; padding null maxima: 2.4790868e-08.
Algebraic sanity references only (not executed fixtures): order-sensitive 1-cosine = 0.28571429 from [1,2,3] vs [3,2,1]; loss degradation = 1 from (2-1)/abs(1).
Permutation formula-gap candidate thresholds: {'strict': 0.002857167400101974, 'balanced': 0.01428573783703869, 'lenient': 0.028571450883209587}. Numerical denominator floors: low 1e-8 / medium 1e-7 / high 1e-6; higher floor is the stricter guard and marks more relative results undefined.
Effect thresholds lack independent calibration controls; user accepted the recommendation to defer freeze.
Bootstrap: paired seed/domain/source-record, 10,000 resamples, 95% percentile candidate intervals.
Several count arms have only one eligible domain and one source record; those intervals cannot establish cross-domain uncertainty or justify freeze.
Experiment Scientist: reproducibility/aggregation suitable for candidate evidence; numerical freeze unsupported.
QA history: pre-remediation CONDITIONAL PASS. Remediation QA: PASS; candidate evidence is usable for user review. Threshold/guard/uncertainty freeze evidence remains insufficient. This is not Stage 03 final QA or closure.
Implementation self-check after remediation: focused 19 passed/1 CUDA skip; full 55 passed/3 CUDA skips; governance/notebook/diff checks passed. This is not independent QA.
Raw rows and checkpoints remain under ignored `outputs/stage03/`.
