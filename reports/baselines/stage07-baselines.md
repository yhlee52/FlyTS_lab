# Stage 07 architecture baseline report

Synthetic-only checks. No loss values, runtime or performance ranking.

| Backbone | Role | H | Parameters | Absolute deviation | Deviation % | Within 5% | Shared equality fingerprint |
|---|---|---:|---:|---:|---:|---|---|
| fly_sparse | reference | 128 | 68760 | 0 | 0.000% | True | `bd617f0dddc6be024eaef819707f646e27913903bbcae9f8cf417f913452546e` |
| dense_leaky | role_diagnostic | 98 | 68530 | 230 | -0.334% | True | `bd617f0dddc6be024eaef819707f646e27913903bbcae9f8cf417f913452546e` |
| gru | formal_candidate | 43 | 68853 | 93 | 0.135% | True | `bd617f0dddc6be024eaef819707f646e27913903bbcae9f8cf417f913452546e` |

All three arms passed the fixed-mask synthetic forward, backward, update, checkpoint resume and adapter checks. The JSON records shapes, parameter schemas, source/config hashes and bounded compute formulas. CUDA remains unverified.
