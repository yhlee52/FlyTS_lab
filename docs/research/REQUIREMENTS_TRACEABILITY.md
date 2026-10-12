# Requirements Traceability

Stage 09 protocol-v2 note (DEC-051): its historical, unfrozen formal proposal targeted R-01/R-02,
R-04 and R-05 through H-01–H-03 and a 60-run matrix. H-04/HARTH and GRU formal
comparisons are excluded/not tested; their earlier engineering/audit evidence is
historical only.

The evidence-stage column in the historical rows below does not authorize Phase
02 execution. DEC-072 assigns prospective owners and gates after the table.

| ID | Requirement | Registered verification and budget | Evidence stage | Claim boundary | Status |
|---|---|---|---:|---|---|
| R-01 | One checkpoint handles variable channel counts. | Shape tests plus deterministic nested unseen/nearest-seen views; paired relative domain-macro Smooth L1 degradation; interpolation/extrapolation separate; 3/5 paired seeds where comparative. | 0, 3, 6, 9 | Supported paired-view range and admitted public domains only; unpaired datasets are descriptive. | Stage 03 development evidence remains descriptive; Stage 09 closed `HOLD` before formal/final inference, so no support result |
| R-02 | Global representation is channel-order invariant. | Deterministic paired permutations; `1-cosine` primary and relative L2 diagnostic; Stage 03 threshold calibration. | 3, 9 | Global representation only; numerical pass rule requires separately approved reopened calibration/freeze. | Stage 03 development distances remain descriptive; Stage 09 closed `HOLD` with the numerical rule unfrozen and no support result |
| R-03 | Metadata is optional. | Signal-only runs using frozen manifests and the common domain-macro protocol. | 0, 6, 9 | Optional metadata support, not equivalence of metadata-rich and signal-only quality. | implemented; broader validation pending |
| R-04 | Missing channels are supported and trained for. | Leakage tests plus paired 0/10/30/50% dropout degradation; matched steps/exposure. | 2, 3, 9 | Registered channel-removal corruption only. | Mechanics and development evidence recorded; Stage 09 closed `HOLD` before formal/final robustness inference, so no support result |
| R-05 | Fly topology effect is isolated. | Primary paired domain-macro Smooth L1 (`beta=1.0`) versus both rewired and random; single-factor study; ±5% parameters; matched optimizer steps, exposure, tokenizer, router, and backbone capacity; five formal seeds. | 4, 5, 9 | Registered controls and budgets only; secondary outcomes cannot substitute for the primary topology endpoint. | Stage 05 controls remain accepted engineering evidence; Stage 09 closed `HOLD` before formal topology inference, so no topology-effect result |
| R-06 | Training runs on CPU and CUDA. | Device-specific backward/checkpoint tests with recorded hardware and environment. | 0, future hardware gate | CPU evidence does not imply CUDA behavior. | CPU recorded; CUDA pending |
| R-07 | Training is possible in a closed network. | No-network pipeline and final offline transfer verification with hashes. | 0, 10 | Recorded bundle and dependency set only. | Stage 10 M8 passed no-index install, socket-blocked pipeline, CPU resume/embed and bundle verification; DEC-070 stopped public release without changing this engineering evidence |
| R-08 | Semiconductor adaptation follows public-data validation. | User stage gate after the public-data evidence package and Phase 02 closeout. | after 19 and separate PI gate | No semiconductor suitability or transfer claim before that gate. | deferred by design; Stage 10 engineering closeout did not satisfy the scientific gate |
| R-09 | Formal evidence is preregistered before results. | Hashed protocol, endpoints, guards, uncertainty/multiplicity rules, seeds, arms and compute freeze with independent QA. | 11–14 | Valid only for the exact frozen version; any material change creates a new version before execution. | Stage 13 PI `HOLD` (DEC-099); no protocol v3, budget or pre-freeze QA; formal Stage 14 blocked. DEC-114 approved a separate synthetic engineering Charter for static preparation only; exact execution remains gated. |
| R-10 | Checkpoint selection is development-only and reproducible. | One frozen selection metric/policy, complete candidate ledger, exact provenance and no final-data influence. | 15–16 | At most one private candidate; selection does not imply publication or foundation-model qualification. | Phase 02 plan proposed; no new checkpoint authorized |
| R-11 | Final evidence is opened once and cannot tune the model. | Atomic access ledger, pre-authorized orchestration, locked sufficient statistics and independent QA. | 17–18 | No reranking, threshold change, added seed/domain or automatic rerun after opening. | Electricity remains sealed; gate pending |
| R-12 | Foundation-model and connectome claims follow an evidence ladder. | Q0–Q3 mapping from H-01–H-04, reproducibility and matched controls. | 11, 19 | Bounded tested-domain claim only; H-03 is required for connectome-specific benefit and H-04 for foundation-encoder evidence. | Stage 11 contract PI `GO` (DEC-074); Stage 13 `HOLD`; DEC-112 engineering route can support Q0 only; Q1–Q3 unachieved |

## Prospective Phase 02 stage and evidence ownership (DEC-072)

| ID | Stage 12/13 decision input | Later evidence owner and gate |
|---|---|---|
| R-01 | Stage 12 Data measures independent paired seen/unseen channel-count views; Stage 13 Experiment freezes the supported range and rule. | Stage 14 QA rehearses; Stages 15–16 Experiment records paired outcomes; Stage 18 final use requires Stage 17 unseal; Stage 19 limits count claims to tested views. |
| R-02 | Stage 12 Data checks paired permutation eligibility; Stage 13 Experiment freezes the global-representation endpoint and rule. | Stage 14 QA validates view identity; Stages 15–16 Experiment reports bounded invariance; final use requires Stage 17 gate. |
| R-03 | Stage 12 Data checks signal-only schema; Stage 13 Experiment registers a metadata-absent path. | Stage 14 Implementation/QA rehearses and Stages 15–16 Experiment records actual signal-only use; optional metadata does not imply equal quality. |
| R-04 | Stage 12 Data checks missingness and paired dropout coverage; Stage 13 Experiment freezes corruption and harm rules. | Stage 14 QA checks leakage; Stages 15–16 Experiment reports matched H-02 outcomes for registered corruption only. |
| R-05 | Stage 12 Data checks domain adequacy; Stage 13 Experiment freezes both topology controls, single-factor terms and budget tolerance. | Stage 14 QA verifies graph/provenance and matching; Stages 15–16 Experiment analyzes both primary contrasts; Stage 19 Q3 needs Q2 plus support against both. |
| R-06 | Stage 13 declares the exact device environment and budget; CPU evidence is already recorded. | Stage 14 Implementation/QA validates any intended CUDA environment before Stage 15; Stage 15 Experiment records device-specific execution. No CUDA claim without it. |
| R-07 | Stage 13 states offline environment/dependency assumptions; Stage 10 M8 is bounded historical engineering evidence. | Stage 14 Implementation/QA repeats no-network preflight for the frozen package; later evidence binds only the tested bundle. |
| R-08 | Stage 12–19 remain public-data work. | Stage 19 Director/QA records the phase result; semiconductor work needs a separate subsequent PI gate. |
| R-09 | Stage 12 adequacy precedes Stage 13 Experiment/Program Integrator protocol v3 and budget packet. | Independent Stage 13 QA `PASS` and explicit PI protocol/budget `GO` precede Stage 15; a material change needs a new approved version. |
| R-10 | Stage 13 Experiment freezes one development-only selection policy. | Stages 15–16 Experiment keeps a complete candidate ledger and chooses at most one private candidate; Stage 16 QA and PI review precede later readiness. |
| R-11 | Stage 13 freezes final-use rules; Stage 17 Data/Experiment/QA audits candidate, source and sealed access. | Separate Stage 17 PI H-04/final `GO` precedes Stage 18 one-time Experiment/QA opening; Stage 19 records any invalid or skipped path. |
| R-12 | Stage 11 Director defines Q0–Q3; Stage 12–13 set eligibility and preregistered rules without assuming support. | Stage 19 Director/QA maps only valid evidence; Q2 needs admitted-target H-04 support, Q3 additionally needs H-03 support against both matched controls. |

Stage 11 approves no source, split, seed, numerical threshold, arm or budget. The
Stage 09 `HOLD`, final QA `FAIL` and report hashes stay historical. No Stage 12
data work follows automatically from acceptance of the Stage 11 result.
