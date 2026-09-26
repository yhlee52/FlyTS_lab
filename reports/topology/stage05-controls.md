# Stage 05 topology controls

Synthetic structural evidence only; no performance or biological claim.

Source commit: `f46093f1dccb717561c6476fbaedf75f11f13198`. Reproduce: `git checkout f46093f1dccb717561c6476fbaedf75f11f13198 && python tools/report_topology_controls.py --source-commit f46093f1dccb717561c6476fbaedf75f11f13198`.

| Kind | Edges | Components | Hash | Retained fraction | Jaccard | Zero outdegree |
|---|---:|---:|---|---:|---:|---:|
| fly_like | 613 | 1 | `ce043facf727493a7220f9939d2214f4ce7d6885406dec950326e970aafb7850` | 1.000000 | 1.000000 | 0 |
| degree_preserving_rewired | 613 | 1 | `aa5014ea2c9012cc5e226c0d1003d570731a20b7d16f926999ee3e50275de45f` | 0.274062 | 0.158790 | 0 |
| random_sparse | 613 | 1 | `013bb0a2a0559891bb70da5dee17ebc841a9e38f3fb2a42d8429adbce88797f4` | 0.135400 | 0.072616 | 0 |

The retained fractions and Jaccard values are descriptive; they were not used to select graphs.
