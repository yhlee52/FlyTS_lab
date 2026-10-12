# Stage 14 Charter — bounded engineering preflight

Status: approved

PI selected this narrow route in DEC-112 and approved this Charter in DEC-114.
The formal Stage 13 protocol/budget freeze remains `HOLD` under DEC-099/110.
This Charter governs an **engineering track only** within Stage
14; it cannot satisfy the formal Stage 14 handoff or Stage 15 entry.
Initial independent document QA was `CONDITIONAL PASS` on `1950938`; its
[condition and Director correction](CHARTER_QA_REPORT.md) are recorded without
claiming an independent delta `PASS`.

## Research question

Can the current CPU runner, reporter and artifact path complete a deterministic,
closed-network rehearsal on synthetic inputs while rejecting sealed and
undeclared inputs, preserving exact provenance and replaying failures?

## In scope for execution after the separate exact-run GO

- One declared synthetic fixture family, tiny CPU forward/backward and
  save/load/resume paths, and the declared topology/control code paths. These
  check mechanics and matching assertions, not topology effect or model quality.
- Synthetic permutation and paired-mask identity, integer channel-removal
  accounting (including a zero-removal case), sufficient-statistic and
  reporter-replay adversarial cases.
- Pre-load raw-byte hash checks for the role registry to catch CRLF worktree
  drift; fail-closed role/test/Electricity path checks before any data loader.
- Local closed-network check, exact CPU/Python/dependency environment capture,
  elapsed time and peak memory/disk accounting, cache/checkpoint/resume and
  failure-ledger tests. Synthetic outputs and checkpoints stay ignored locally.

## Out of scope

- Any real source signal or mask read, new dataset search/download/admission,
  formal training/evaluation, development score inspection, Electricity or any
  test opening, target task, CUDA support claim, private candidate selection,
  public release or semiconductor transfer.
- H-01–H-04 support claims, Q1–Q3 qualification, formal Stage 14 completion,
  Stage 15 execution, and retrospective repair of Stage 09 reports or hashes.
- Relaxing the original Stage 13 acceptance criteria or treating Stage 08/10
  engineering observations as a frozen Phase 02 formal protocol.

## Inputs

- Approved Stage 11 contract and Stage 13 Charter/RESULT, DEC-099/110/112.
- Existing tracked code/config and synthetic test fixtures only, bound to one
  reviewed Git commit; no `data/` or **preexisting** `outputs/` input path.
  A checkpoint generated inside the same approved synthetic run may be read
  once for its declared resume check.
- The historical Stage 09 unfrozen matrix may be reused only as an immutable
  **synthetic fixture selector**. Its run count, seeds, thresholds and claim
  rules are not adopted as a Phase 02 protocol or budget.
- A preflight manifest proposed before execution: exact commands, source/config
  and fixture hashes, dependency lock, seed, CPU environment, timeout, storage
  location and resource cap. Propose numerical limits from a conservative
  device bound and obtain PI approval before any model-executing test or smoke
  measurement; none is frozen by this proposal. A preliminary measurement,
  if later needed, requires its own exact PI run approval first.

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| Exact preflight manifest and bounded CPU resource request | `docs/research/stages/stage-14/PREFLIGHT_MANIFEST.md` or versioned config | Director/Implementation |
| Minimal guard, runner/reporter and synthetic-fixture changes; test code prepared before execution | `src/flyts/`, `tools/`, `tests/`, as needed | One Implementation owner |
| Ignored local execution log, hashes, failure ledger, resource record | `outputs/` only | Implementation |
| Result and independent QA | `docs/research/stages/stage-14/RESULT.md`, `QA_REPORT.md` | Director, independent QA |

## Acceptance criteria

- [x] PI approves this exact engineering-only Charter and a bounded QA/agent
  budget; its formal-stage limitations appear in traceability and current state.
- [ ] Before execution, a reviewed manifest binds one code commit, commands,
  fixture/config/dependency hashes, CPU environment, seed, timeout and
  memory/disk cap. PI approves that exact cap and run.
- [ ] Independent pre-execution QA verifies no real-array path, network access,
  Electricity/test resolution or live-config fallback is possible; registry
  byte mismatch fails before loader use.
- [ ] Declared synthetic cases pass deterministic pair identity, integer mask,
  topology/control matching, cache, checkpoint/resume, failure-ledger and
  reporter replay checks. Invalid hashes, seed aliases, nonfinite data and
  undeclared inputs fail closed.
- [ ] The run stays within the approved resource cap and records exact
  environment, time, memory/disk and output hashes. Independent result QA
  reports `PASS`, `CONDITIONAL PASS` or `FAIL` with omitted checks explicit.
- [ ] The result labels H-01–H-04 `not tested`, keeps Stage 13 formal freeze
  `HOLD`, Q0 as highest possible level, Stage 15 `NO GO`, sealed assets intact
  and DEC-070 release `STOP`.

## Ordered work

| Unit | Work | Gate |
|---|---|---|
| 0 | Director finalizes this Charter, scope crosswalk and resource-measurement method. | Independent document QA, then PI Charter/QA-budget `GO`. No execution before this. |
| 1 | One Implementation owner prepares exact synthetic fixture, fail-closed guards, manifest and focused test code. Static/document checks only; new model-executing cases must not be collected by automatic PR CI before the exact run `GO`. No smoke measurement or checkpoint. | Independent pre-execution QA and PI `GO` for exact CPU cap/run. |
| 2 | Run the approved focused tests and declared synthetic preflight only; capture ignored artifacts and failure ledger. | Stop on source/seal/network/hash violation or cap breach; no automatic retry. |
| 3 | Director writes bounded result and notebook; independent QA checks replay and claim limits. | PI accepts engineering result. Formal Stage 13/14 and Stage 15 gates remain separate. |

## User checkpoints

| Decision gate | Required before | State |
|---|---|---|
| Engineering Charter and QA staffing | Unit 1 implementation | QA staffing `GO` DEC-113; Charter `GO` DEC-114 |
| Exact synthetic manifest, CPU cap and execution | Unit 2 run | **HOLD**, DEC-115: no existing runnable offline CPU environment; exact QA/PI run GO absent |
| Engineering result acceptance | Any later engineering claim | pending after independent result QA |

## Agent plan and budget proposal

- Director owns Charter, decisions, scope crosswalk and result.
- One Implementation owner may edit the preflight code path after Charter GO.
- One independent QA reviewer performs one Charter review, one exact-manifest
  pre-execution follow-up and one result follow-up; QA does not edit tracked
  files. The existing Stage 13 reviewer follow-up allowance is exhausted, so
  this new scoped budget was **approved in DEC-113** before activation.
- No Data or Experiment specialist is needed for this engineering-only path.

```yaml
agent_budget:
  default_mode: single_agent
  max_specialists: 2
  max_parallel_agents: 2
  max_debate_rounds: 0
  max_followups_per_agent: 2
  max_agent_report_words: 500
  user_approval_for_expansion: true
```

CPU compute and wall-time cap: **unselected; execution HOLD (DEC-115)**.
No GPU or new data budget is proposed.

## Risks and stop conditions

Real-data path resolution, source/test/Electricity read, network request,
registry/worktree hash mismatch, undeclared input, reporter replay failure,
resource-cap breach or missing independent QA produces `HOLD`/`FAIL` and stops
the run. Repair requires a new manifest, QA and PI review. A synthetic success
is only engineering evidence and never replaces held-out H-01 count coverage.
The proposed Python socket guard does not block every possible non-Python
network path, and proposed memory/disk checks observe each completed row rather
than enforce an OS-level hard limit. The exact run packet must describe these
limits and obtain PI acceptance or add stronger controls before execution.

## User approval

- Narrow route A: selected, DEC-112.
- QA staffing: **GO**, DEC-113; Charter: **GO**, DEC-114. Exact resource cap
  and execution: **HOLD**, DEC-115; no existing offline CPU environment.
- Formal Stage 13 freeze, Stage 15, final/test opening and release: **not
  approved**.
