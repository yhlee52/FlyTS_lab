# FlyTS Current Research State

Updated: 2026-09-28

## Current stage

Stage 08 is closed under DEC-035 after the operational pilot, independent QA
`PASS` and PI result `GO`; DEC-036 authorizes Draft PR preparation and CI, on
`codex/stage-08-flyts-mini-pilot`, based on
GitHub `main` merge commit `34b83c29d8a5588158d1e4abe420bfc8cbdf5e68`.
Stages 00–08 are closed. The Stage 08 branch remains unmerged. Numerical
robustness settings remain candidate.

## Current goal

Commit and push the closed Stage 08 evidence, open a Draft PR and verify CI. Do not
merge, rerun, access final-held-out data or start Stage 09.

## Canonical references

- `docs/DEVELOPMENT_PLAN.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/PROJECT_CONSENSUS.md`
- `docs/DATASETS.md`
- `docs/BACKBONES.md`
- `docs/TOPOLOGY_CONTROLS.md`
- `docs/research/TEAM_CHARTER.md`
- `docs/research/TOKEN_BUDGET_POLICY.md`
- `docs/research/stages/stage-08/CHARTER.md`

## Confirmed decisions

- The user remains the final `GO`, `REVISE`, `HOLD` or `STOP` authority.
- PR #13 is merged into `main` at `34b83c2`; Stage 07 evidence and QA remain unchanged.
- Stage 08 is an operational pilot and cannot support topology/backbone superiority,
  robustness pass/fail, foundation, transfer, CUDA or semiconductor claims.
- Core arms are fly-like, degree-preserving rewired, random sparse and GRU; dense
  leaky is a short diagnostic only.
- Core budget is one seed and 400 steps split `200 + resume + 200`; dense is
  `10 + resume + 10`.
- Use Stage 07 sizes/profile with temporal/channel/dropout masking `0.4/0.2/0.1`,
  AdamW `5e-4`, batch 8, context 256, stride 128, four CPU threads and float32.
- Base/topology seed is 7 and topology-control seed is 5007.
- Appliances and Beijing are pretrain-only; Bike is development evaluation-only;
  Electricity is sealed until the separately frozen Stage 09 protocol.
- `best.pt` is selected only by exact pretrain validation `L_select`; Bike never
  selects checkpoints or settings.
- Resource evidence is a single descriptive CPU measurement. Stage 09 costs are
  400/2,000/50,000-step five-seed scenarios, not a budget choice.
- The PI accepted the bounded Stage 08 operational result under DEC-035; this does
  not authorize a Draft PR, merge, Stage 09 or final-held-out access.
- DEC-036 authorizes the Stage 08 commit, branch push, Draft PR and CI observation;
  merge remains a separate gate.
- Experiment, one implementation owner and independent QA are the only planned
  specialists; Data requires a separate budget/substitution gate.

## Open questions

- Whether to merge the Stage 08 Draft PR after CI passes.
- Stage 09 requires its own charter, frozen budget and explicit `GO`.
- When suitable CUDA hardware becomes available; CUDA remains unverified.

## Active risks

- Final-held-out/test access or Bike-driven selection would invalidate later evidence.
- High-channel padding and full evaluator paths may exceed memory; OOM is `HOLD`.
- In-place resume can overwrite its input; Stage 08 preserves and hashes a snapshot.
- Candidate numerical settings can be mistaken for frozen robustness thresholds.
- Single-run CPU timing cannot establish comparative efficiency or guaranteed cost.
- The report CLI requires a resolved absolute runs path to match bound execution paths.

## Latest evidence

- Stage 07 final QA is `PASS`; core matched sizes are Fly 68,760, dense 68,530 and
  GRU 68,853 parameters with shared front-end/head count 27,208.
- GitHub PR #13 merged at `34b83c2`; its tree matches the reviewed Stage 07 head.
- Stage 06 canonical manifest/registry hashes remain `44bafe48…e7f6c` and
  `0095d4cd…b9b20`; final-held-out model performance has not been inspected.
- The current environment is Python 3.12.14, PyTorch 2.14.0+cpu with no CUDA device.
- The first preflight attempt exposed a runner epoch-boundary defect and is preserved.
- Its one allowed same-config diagnostic rerun completed all four core arms with two
  finite optimizer steps, 16 samples, approved parameter counts, preserved resume
  hashes, a common Bike-only fixture and no observed final-held-out access.
- Before DEC-028, focused/full tests, compile and validators passed; CUDA was skipped.
- DEC-028 authorizes one existing-Implementation follow-up and one independent QA
  re-review only; it does not authorize another preflight or the real pilot.
- DEC-028 remediation binds the missing bytes and separates all required timing
  phases; focused tests and validators pass, and schema-v1 evidence is rejected.
- DEC-029 authorizes one further existing-Implementation follow-up and one further
  independent QA re-review only; it does not authorize any execution.
- DEC-029 closes execution-fact validation; 19 focused tests and the full local
  suite pass, with three CUDA skips.
- DEC-030 authorizes one final history-independent archival-test fix and QA
  re-review only; no public execution is authorized.
- Final DEC-030 independent code QA is `PASS`: exact archival hashes, schema-v2
  execution facts, focused/full suites, compile, validators and Git hygiene pass.
- DEC-031 authorizes exactly one new schema-v2 common preflight for the four core
  arms; dense and the real pilot remain unauthorized.
- The DEC-031 preflight passed for all four arms: schema 2, two steps, 16 samples,
  approved parameters, finite histories, preserved resume input and one Bike fixture.
- Strict report generation and `--check` matched; report hashes are recorded in
  `docs/research/stages/stage-08/PREFLIGHT_RESULT.md`.
- DEC-032 authorizes one fixed-order real pilot plus dense diagnostic; reruns,
  final-held-out access and Stage 09 remain unauthorized.
- The DEC-032 pilot completed once at
  `outputs/stage08-pilot/pilot-20260927-v1/`: every core arm recorded 400 steps and
  3,200 samples, and dense recorded 20 steps and 160 samples, with finite histories,
  approved parameter counts, preserved resume inputs and Bike-only evaluation.
- Strict schema-v2 report generation and byte-stable `--check` pass. The tracked
  reports are `reports/PILOT_RESULTS.json` and `reports/PILOT_RESULTS.md`.
- Individual core `L_select` values are 0.971362 (fly-like), 0.971023 (rewired),
  0.970546 (random sparse) and 0.960195 (GRU); dense diagnostic is 0.985048. These
  are descriptive single-seed observations only.
- Rewired setup dominated its measured CPU path; this is a cost-risk observation,
  not topology performance evidence. Stage 09 scenarios remain linear estimates.
- The complete local suite passes with three CUDA skips; compile, report replay,
  notebook/governance, diff and ignored-artifact checks pass.
- Independent post-pilot QA is `PASS` with no blockers. QA independently matched
  all 15 checkpoint/snapshot hashes, execution facts, selection, Bike-only scope,
  provenance replay, focused/full tests, compilation and artifact hygiene.
- DEC-035 records the PI result `GO` on 2026-09-28 and closes Stage 08 within its
  operational/descriptive claim boundary.
- DEC-036 records option A `GO` for commit, Draft PR creation and CI only.

## Next action

Create the Stage 08 Draft PR, verify CI and return to the merge gate. Stage 09 and
final-held-out access remain separately unauthorized.
