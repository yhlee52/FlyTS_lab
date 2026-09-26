# Stage 05 Charter — Topology Controls

Status: review

## Research question

Can `fly_like`, `degree_preserving_rewired`, and `random_sparse` be generated,
validated, restored, and exercised through the same graph artifact and Foundation
model path under a preregistered structural, seed, and provenance contract without
making a topology-performance claim?

## In scope

- Add exact directed degree-preserving rewiring and fixed-edge random sparse controls.
- Keep node/edge count, population assignment, model path, and trainable-parameter
  contract matched across all three arms.
- Add deterministic structural fixtures, graph reports, checkpoint/run provenance,
  and exact config-to-buffer validation.
- Run synthetic CPU forward, backward, and one optimizer step only.
- Complete independent QA, research records, and a Draft PR.

## Out of scope

- Performance-ranked seed or graph selection, post-hoc structural rules, mini-training,
  topology ranking, robustness pass/fail, or any foundation/topology/transfer claim.
- Topology-specific tokenizer, router, backbone, decoder, masking, width, population,
  parameter, optimizer, step, exposure, or schedule changes.
- Test/final-held-out access, Stage 06 corpus work, Stage 07 baselines, CUDA claims,
  biological-validity claims, PR auto-merge, or automatic Stage 06 start.

## Inputs

- Base `origin/main` commit `944f8ed`; Stage 04 PR #10 is merged.
- `docs/research/stages/stage-04/{CHARTER,RESULT,QA_REPORT}.md` and the Stage 04 fixture.
- `docs/{TOPOLOGY,ARCHITECTURE,EXPERIMENT_PROTOCOL,DEVELOPMENT_PLAN}.md`.
- H-03, R-05, DEC-007/014–018, and RK-03/08/09/11/18–21.

## Topology control contract

- `degree_preserving_rewired` performs directed double-edge swaps on the reference
  fly-like graph. It preserves every node's in/out degree and the weak-component
  count, rejects loops/duplicates/no-ops, and accepts exactly `10E` uniformly
  proposed valid swaps within `200E` attempts. The final graph must differ from the
  reference; retained-edge fraction and Jaccard are descriptive, not pass/fail gates.
- `random_sparse` samples exactly `E` loop-free directed pairs without replacement.
  It conditions only on incoming coverage, the reference weak-component count, and
  not exactly matching both reference degree sequences. It permits at most 256
  deterministic candidate attempts; zero-outdegree nodes are allowed and reported.
- Neither control changes seed after failure or selects among successful candidates.
  Exhaustion of the accepted-swap/candidate attempt budget remains a user `HOLD`.
- Population and module labels remain identical. Controls do not use module labels
  for generation; edge types are recomputed and actual incoming degree normalizes
  recurrence. Reciprocity, modularity, mixing, overlap, Jaccard, and degree distances
  are descriptive.

## Seed and provenance contract

- Existing training `seed` behavior remains unchanged. `topology_seed` determines
  the shared reference fly-like graph.
- New `topology_control_seed` is required for control topologies. A SHA-256 namespace
  `flyts-topology-control-v1/{kind}/{seed}` produces the actual 63-bit generator seed.
- One config determines one graph. Graph builders use local generators and may not
  consume global model-initialization RNG.
- `run.json`, additive format-v1 checkpoint metadata, and the tracked Stage 05 report
  record kind, schema, content hash, reference/control/resolved seeds, parameters,
  structural statistics, source commit, environment, and reproduction command.
- Loading regenerates the expected graph and exactly checks the five graph buffers.
  Legacy fly-like v1 checkpoints remain strict-loadable; missing control metadata on
  new controls, config/buffer mismatch, and cross-topology resume are rejected.

## Deliverables

| Deliverable | Path | Owner |
|---|---|---|
| Builders, registry, validation, statistics | `src/flyts/topology/` | Implementation |
| Model/checkpoint/evaluator integration | `src/flyts/{foundation,training,evaluation}.py` | Implementation |
| Structural and CPU integration tests | `tests/test_topology_controls.py` plus fixture | Implementation |
| Deterministic report config/tool | `configs/topology/`, `tools/report_topology_controls.py` | Implementation |
| Interface and control contract | `docs/TOPOLOGY_CONTROLS.md` | Director / Implementation |
| Small committed evidence | `reports/topology/stage05-controls.{json,md}` | Implementation |
| Independent verification and result | `docs/research/stages/stage-05/` | QA / Director |

Raw graph masks, checkpoints, training outputs, and large artifacts are not committed.

## Acceptance criteria

- [x] Stage 04 fly-like hashes, state keys, parameter order/count, and strict legacy
  format-v1 behavior remain unchanged.
- [x] All arms have exact matched N/E, population/module annotations, trainable
  parameter names/order/shapes/count, and deterministic graph hashes.
- [x] Rewired has exact nodewise in/out degrees, component count, `10E` uniformly
  proposed accepted swaps within `200E` attempts, and a different final edge set;
  overlap and Jaccard are reported descriptively.
- [x] Random has exact N/E, valid incoming coverage and component count, and does not
  duplicate both reference degree sequences.
- [x] Builders do not alter global RNG; paired model initialization is bitwise equal.
- [x] Dense/scatter use the same model path and complete finite CPU forward, backward,
  and one optimizer step for every arm without reporting relative performance.
- [x] Format-v1 legacy/new loads, exact graph provenance, buffer mismatch rejection,
  and cross-topology resume rejection are tested.
- [x] The tracked JSON/Markdown report is byte-stable under `--check`; focused/full
  tests, notebook/governance validators, and `git diff --check` pass.
- [x] Independent QA reports `PASS` or user-reviewable `CONDITIONAL PASS`; no scientific
  claim or Stage 03 candidate threshold is used.

## User checkpoints

| Decision gate | When to ask | Current approval |
|---|---|---|
| Stage Charter and numeric contract | Before implementation | GO, 2026-09-26 |
| Material scope/criteria/seed/budget change | Before affected work | HOLD if encountered |
| Overlap-guard revision | Before resuming implementation | GO, 2026-09-26 (DEC-019) |
| Constraint infeasibility | Before changing a seed or rule | pending as needed |
| Extra QA remediation follow-up | Before a second post-FAIL re-review | GO, 2026-09-26 (DEC-020) |
| Stage result | After independent QA | pending user decision; QA `PASS` |
| Merge or Stage 06 | After result gate | separately pending |

## Agent plan

- Primary owner: Research Director, retaining experiment/fairness contract authority.
- Architecture Scientist: bounded read-only feasibility and invariant review.
- Implementation Engineer: sole tracked-code writer after the architecture handoff.
- QA Engineer: independent rerun and review; no tracked implementation edits.
- Experiment Scientist is not activated because Stage 05 contains no performance study.

## Budget

```yaml
agent_budget:
  default_mode: single_agent
  max_specialists: 3
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 1  # Stage 05 QA only: one extra follow-up approved in DEC-020
  max_agent_report_words: 700
  user_approval_for_expansion: true
```

## Risks and stop conditions

- Stop with `HOLD` if a registered fixture cannot satisfy the fixed contract, any
  fly-like hash/state/parameter contract changes, global RNG is consumed, format-v1
  requires a bump/non-strict load, or fairness/scope/seed/budget needs revision.
- Stop on test/final-held-out access, performance comparison, Stage 06/07 work, or an
  unresolved independent QA `FAIL`.
- H-03 performance, robustness thresholds, transfer, CUDA, biological mechanism,
  foundation quality, and semiconductor suitability remain `미검증` after Stage 05.

## Hold evidence

- The approved `N=64`, `E=613`, base-seed 7, control-seed 5007 fixture completed
  exactly `10E = 6,130` valid component-preserving directed swaps but retained
  `168/613 = 0.274062` reference edges, above the preregistered `0.10` maximum.
- Implementation and Architecture independently found no straightforward orientation,
  bookkeeping, degree, duplicate, component, or overlap-calculation defect.
- The diagnostic prototype was reverted. No control implementation, test fixture,
  report, training run, performance result, or QA verdict was retained.
- Changing the proposal policy or overlap acceptance rule requires a revised user GO.

## Hold resolution

- On 2026-09-26 the user approved retaining uniform `10E/200E` swaps and exact
  degree/component guards while making overlap and Jaccard descriptive.
- This revision avoids selecting a graph or proposal policy to optimize observed
  overlap. The failed `0.10` result remains recorded above and implementation resumes
  under DEC-019.

## QA remediation status

- Initial QA `FAIL` found that the report called base commit `944f8ed` its source
  even though that commit lacked the control implementation. Source and report
  commits are now separated, source paths are hash-recorded, and report reproduction
  validates the recorded source commit.
- The first allowed QA follow-up `FAIL` found incomplete training reproduction argv
  for resume, epoch overrides, and development-only runs. The command builder and
  regression test are corrected; targeted tests, the full self-check suite, report
  check, validators, and diff check pass.
- DEC-020 approves one additional independent QA follow-up. The stage is active for
  that bounded final verification only.

## User approval

- Decision: GO, revised by DEC-019; QA budget exception DEC-020
- Date: 2026-09-26
- Conditions: implement the uniform-rewiring revised contract through independent QA
  and a Draft PR only; do not merge or begin Stage 06 without a separate user decision.
