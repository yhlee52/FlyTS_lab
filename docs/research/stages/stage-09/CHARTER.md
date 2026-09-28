# Stage 09 Charter — Formal Study

Status: hold

Gate detail: **DEC-057 QA FAIL; PI accepted HOLD closure and Draft PR under DEC-058**

Protocol version: **2 — H-01–H-03 / 60-run unfrozen proposal (DEC-051)**

Approval boundary: the PI approved the H-01–H-03 scope revision, 60-run option
and DEC-054 bounded M1 calibration on 2026-09-28. This authorizes six 400-step
development runs and synthetic 4/18/370 fixtures, but not M2 numerical freeze,
M5/M6, Electricity access, a final claim or H-04/HARTH/GRU formal scope.

## Research question

Can a completely frozen, leakage-safe public-data study produce valid bounded
evidence for H-01 through H-03 across registered graph and training seeds, while
keeping Electricity final-held-out evidence sealed until independent QA and a
separate PI gate?

## In scope

- Stage 9A development-only H-01/H-02 calibration, H-03 statistical fixtures,
  protocol drafting, formal tooling, blind rehearsal and fresh protocol-v2 QA.
- A proposed Stage 9B matrix of 45 topology runs and 15 temporal-only Fly masking
  controls on CPU float32, subject to later freeze and PI approval.
- Deterministic graph caching with exact equivalence checks, formal provenance,
  record/subject-level sufficient statistics, locked analysis and one-time unseal
  tooling that cannot open final assets during Stage 9A.
- Explicit `support`, `no-support`, `harm`, `inconclusive`, `not tested` and
  `invalid due to protocol failure` outcome boundaries.

## Out of scope

- Formal pretraining, final-held-out/test access, performance interpretation,
  result-driven reruns, PR merge, Stage 10, checkpoint publication,
  CUDA claims and semiconductor claims.
- Changing the existing Appliances/Beijing/Bike/Electricity roles, using Bike to
  choose a formal arm/budget/seed, or inventing thresholds when calibration is
  insufficient.
- H-04, HARTH admission/use, frozen probes, transfer claims and GRU formal runs.
  Historical HARTH and GRU evidence remains recorded but cannot enter v2 results.
- Treating windows as independent inferential units or using secondary metrics to
  rescue a failed primary endpoint.

## Inputs and fixed design

- GitHub `main` merge commit `9f41e0fcf55a8b1a606e21bb53c1220bdc57dfc3`;
  its tree matches the reviewed Stage 08 PR head.
- Stage 06 manifest `44bafe48196a4afd096e387dc672cad128d390ab7e5b413ea6cbeadf5f3e7f6c`
  and registry `0095d4cd76ad5fdaeefeccdbb4322187892cc155bfac619ca4c8618ea50b9b20`.
- Training seeds `7/17/29/43/59`; topology seeds `7/17/29`; corresponding control
  seeds `5007/5017/5029`.
- Proposed formal budget: 10 epochs of 1,000 steps, process-boundary resume after
  epoch 5, batch 8, 80,000 exposures per run, context 256, stride 128, four CPU
  threads, float32 and the Stage 08 AdamW settings.
- H-02 controls retain temporal masking `0.4` and set channel masking/dropout to
  `0/0`; this tests the combined channel-masking/dropout factor only.
- The v2 matrix is exactly 60 rows: `fly_like`, `degree_preserving_rewired` and
  `random_sparse` × three graph seeds × five training seeds, plus 15 paired
  `temporal_only` rows. GRU and dense-leaky are not formal v2 arms.
- DEC-050 keeps HARTH unadmitted and H-04 `not tested`. Its audit artifacts and
  failed 14/4/4 candidate are historical evidence only.

## Deliverables

| Deliverable | Location | Owner |
|---|---|---|
| M0 integration and research records | `docs/research/`, Stage 08 result note | Director |
| Preserved HARTH HOLD evidence | `docs/DATASETS.md`, this stage folder, ignored audit artifacts | Data / Director |
| H-01–H-03 calibration and 60-row readiness matrix | this stage folder and ignored `outputs/stage09/` | Experiment / Director |
| Formal configs, graph cache, runner and locked reporter | `configs/formal/stage09/`, `tools/`, `tests/` | Implementation |
| Independent pre-freeze review | `docs/research/stages/stage-09/QA_REPORT.md` | QA |
| Non-frozen formal-manifest proposal | proposed under `configs/formal/stage09/` | Director / Implementation |

Raw data, arrays, checkpoints, graph caches, logs and large run artifacts remain
ignored and outside Git.

## Stage 9A milestones

| Milestone | Scope | Owner | Exit condition |
|---|---|---|---|
| M0 | synchronize `main`; reconcile Stage 08 merge and Stage 09 access records | Director | governance and notebook checks pass |
| M1 | preserve HARTH `HOLD`; execute H-01/H-02 development controls and H-03 known-effect fixtures | Experiment | numerical candidates are evidenced, or status is `HOLD` |
| M2 | prepare the exact H-01--H-03 rules and protocol-v2 packet for PI selection | Director / Experiment | every numerical value is explicit; no value is treated as frozen before PI approval |
| M3 | build and blindly rehearse matrix, cache, resume, aggregation, reporting and sealed-access tooling | Implementation | synthetic/development-only tests pass without final access |
| M4 | independently review protocol-to-config fidelity, leakage, replay and access controls | QA | QA records `PASS`, `CONDITIONAL PASS` or `FAIL` |

M5 immutable freeze, M6 formal pretraining, M7 pre-unseal review, M8 final
opening, M9 locked analysis and M10 result review are later work and require the
gates listed below.

## Hypothesis-to-freeze trace

| Hypothesis | Stage 9A evidence and proposed rule output | Blind verification | Later bounded outcome |
|---|---|---|---|
| H-01 | Bike calibration for eight permutations and count views `4/18/370`, with seen counts `11/26`; propose exact invariance, degradation and uncertainty limits | deterministic view identity, record-first aggregation and all-view conjunction fixtures | registered count/view representation behavior only |
| H-02 | Bike paired 0/10/30/50% degradation; propose three effect limits, a 0% harm guard and intervals | masked versus temporal-only single-factor/config and paired-order fixtures | combined channel masking/dropout effect only |
| H-03 | known-effect synthetic graph-cluster fixtures; propose two one-sided upper-bound criteria | graph-outer/training-inner 10,000-resample interval and conjunctive-IUT fixtures | registered topology controls only; no endpoint-winner claim |
| H-04 | excluded by DEC-051 after PI-accepted HARTH admission `HOLD` | historical scanner/audit replay only | `not tested`; no transfer claim |

If any development evidence cannot support an exact candidate or the registered
statistical unit cannot support the intended interval, the corresponding M2 item
is `HOLD`; the implementer must not choose or silently inherit a number.

## Acceptance criteria for Stage 9A

- [x] M0 records PR #14 merged at `9f41e0f` without changing Stage 08 evidence.
- [x] HARTH admission `HOLD`, failed split and no-search history are preserved;
  H-04/HARTH cannot enter the protocol-v2 manifest or results.
- [x] Existing four corpus roles remain unchanged; Electricity stays sealed and
  HARTH registry-v2 admission is prohibited under this protocol.
- [x] Development-only executed controls either justify exact guard/effect/interval
  candidates or produce `HOLD`; no final asset is accessed.
- [x] The proposed 60-run matrix is complete and parameter/steps/exposure/data-order
  contracts are machine validated.
- [x] Graph-cache loads reproduce all graph buffers exactly and reject corruption or
  key/config drift.
- [x] Blind fixtures verify resume, earliest-minimum selection, record-first and
  subject-preserving aggregation, IUT logic, probe controls, atomic unseal and
  byte-stable report replay without final metrics.
- [x] Fresh protocol-v2 QA reports `PASS` under DEC-052; only this bounded v2
  `PASS` may be presented for the separate PI formal-freeze/run gate. Earlier M4
  QA applies to the historical 65-row package only.

## User checkpoints

| Gate | Required before | Current approval |
|---|---|---|
| Stage 9A plan/Charter | M0–M4 implementation | `GO`, 2026-09-28 |
| Bounded M4 tooling result | retain readiness package | `GO`, 2026-09-28 (DEC-045) |
| HARTH admission | any H-04 data use | `HOLD` accepted, 2026-09-28 (DEC-050) |
| Protocol v2 scope/matrix | active Stage 09 proposal | `GO`, 2026-09-28 (DEC-051) |
| Protocol v2 consistency QA | development calibration/M2 packet | `PASS`, 2026-09-28 (DEC-052) |
| Bounded M1 calibration budget | six development runs and synthetic fixtures | `GO`, 2026-09-28 (DEC-054) |
| Final reporter remediation QA | Stage 09 disposition | `FAIL`, 2026-09-28 (DEC-057) |
| Stage 09 HOLD closure | Draft PR and handoff | accepted, 2026-09-28 (DEC-058) |
| Dataset/split/metric/scope/budget change | affected work | `HOLD` if encountered |
| Exact guard/effect/uncertainty freeze | immutable manifest | pending after calibration |
| Stage 9B formal run | M6 | pending after calibration, M2 freeze and M5 review |
| Final open | Electricity access | pending after M7 QA |
| Draft PR | review of preserved HOLD package | authorized, 2026-09-28 (DEC-058) |
| Merge, Stage 10 or claim expansion | any integration/next stage | pending separate PI decision |

## Agent plan and budget

The Research Director owns decisions and user gates. Five specialist roles are
approved sequentially: Data Scientist, Experiment Scientist, Program Integrator,
one Implementation Engineer and independent QA Engineer. At most two specialists
are active concurrently; specialists do not delegate. Implementation is the only
tracked code writer and QA modifies no tracked files.

```yaml
agent_budget:
  max_specialists: 5
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 1
  max_agent_report_words: 700
  user_approval_for_expansion: true
```

Budget exception (DEC-041): after the first M4 `FAIL`, the PI authorized one
additional follow-up turn each for the existing Implementation Engineer and QA
Engineer, limited to nonfinite H-03 rejection and the cache-consuming one-run
orchestration/locked-report rehearsal. No other scope or role is added.

Micro exception (DEC-043): after replacement QA reproduced derived arithmetic
overflow, the PI authorized one final micro follow-up turn each for the same
Implementation and QA owners, limited to derived-finiteness guards and the exact
finite-`1e308` regression. Sufficient-statistic and HARTH scope cannot expand.

HARTH scanner exception (DEC-048): after DEC-047 QA identified subject-cadence
and exact-label defects, the PI authorized one additional bounded Implementation
turn and one independent QA rerun for those defects only. Namespace, seed, split,
metric, admission status and all later gates cannot change.

Final Stage 09 exception (DEC-056): the PI authorized one last Implementation
turn and one independent QA turn solely to create `REPORT-v2.json` from preserved
DEC-054 rows with the registered clean-harm summary. No rerun or new analysis
choice is allowed. After QA, present a direct stage-gate disposition and do not
start another remediation cycle automatically.

## Risks and stop conditions

- Immediate `HOLD` on final/test access, label leakage, ambiguous rights/schema/task,
  infeasible subject coverage, insufficient statistical units, post-result rule or
  seed changes, missing formal arms, CPU/GPU mixing, non-finite values, parameter or
  exposure mismatch, graph-pairing/cache mismatch, provenance drift or frozen-code
  mutation.
- A calibration failure is a valid Stage 9A result and does not authorize reuse of
  the unfrozen Stage 03 candidates.
- A diagnostic rerun requires a preserved instrumentation/data-integrity defect,
  identical config/seed and separate PI authorization.

## User approval

- Decision: `GO` for Stage 9A M0–M4 implementation only.
- Date: 2026-09-28.
- Conditions: implement the supplied plan and preserve the later formal-run and
  final-open gates; do not infer approval from agent agreement or passing tests.
- Remediation: option A approved on 2026-09-28 under DEC-041; HARTH remains `HOLD`.
- Micro-remediation: derived-finiteness guard approved on 2026-09-28 under DEC-043.
- Bounded M4 result: tooling QA `PASS` accepted on 2026-09-28 under DEC-045;
  M1/M2 and all later gates remain unchanged.
- HARTH remediation: option A metadata-only one-shot candidate authorized on
  2026-09-28 under DEC-046. DEC-047 records coverage `HOLD` and QA `FAIL`; no
  admission, alternate split or later gate is authorized.
- HARTH scanner micro-remediation and QA rerun approved on 2026-09-28 under
  DEC-048. DEC-049 reports scanner QA `PASS`; scientific admission stays `HOLD`.
- HARTH admission `HOLD` accepted on 2026-09-28 under DEC-050. H-04 remains
  `not tested`; any replacement target or scope revision requires a new PI gate.
- Protocol v2 approved on 2026-09-28 under DEC-051: active hypotheses H-01–H-03,
  exactly 60 proposed formal runs, H-04/GRU excluded. M2 and later gates remain
  pending, and the historical 65-row M4 QA does not accept the v2 package.
- Bounded M1 calibration option A approved on 2026-09-28 under DEC-054: six
  400-step development runs plus synthetic 4/18/370 fixtures. M2 freeze and all
  later gates remain pending.
- Final reporter-only remediation and QA approved on 2026-09-28 under DEC-056;
  this is the last Stage 09 remediation cycle and cannot rerun training/evaluation.
- Stage 09 `HOLD` closure and a Draft PR were accepted on 2026-09-28 under
  DEC-058. Merge, Stage 10 and every scientific claim remain unauthorized.
