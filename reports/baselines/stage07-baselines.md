# Stage 07 architecture baseline report

Synthetic-only checks. No loss values, runtime or performance ranking.

| Backbone | Role | H | Parameters | Absolute deviation | Deviation % | Within 5% | Shared hash |
|---|---|---:|---:|---:|---:|---|---|
| fly_sparse | reference | 128 | 68760 | 0 | 0.000% | True | `4b1e236fae5786370922382b6f0f85cb1e779591d8c25fa346b238eb8f9ed953` |
| dense_leaky | role_diagnostic | 98 | 68530 | 230 | -0.334% | True | `4b1e236fae5786370922382b6f0f85cb1e779591d8c25fa346b238eb8f9ed953` |
| gru | formal_candidate | 43 | 68853 | 93 | 0.135% | True | `4b1e236fae5786370922382b6f0f85cb1e779591d8c25fa346b238eb8f9ed953` |

All three arms passed the fixed-mask synthetic forward, backward, update, checkpoint resume and adapter checks. The JSON records shapes, parameter schemas, source/config hashes and bounded compute formulas. CUDA remains unverified.
