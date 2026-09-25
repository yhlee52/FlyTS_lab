# FlyTS Current Research State

Updated: 2026-09-25

## Current stage

Stages 00–03 are closed. PR #8 was merged into `main` at `461f1fc`. Stage 03 closed after user-approved no-freeze closure and independent final QA `PASS`; thresholds, numerical guards and uncertainty config remain candidate.

## Current goal

Prepare the user-authorized Stage 03 Draft PR for review. Preserve candidate numerical settings; report descriptive robustness metrics only. Merge and Stage 04 remain separately gated.

## Canonical references

- `docs/DEVELOPMENT_PLAN.md`
- `docs/ARCHITECTURE.md`
- `docs/DATASETS.md`
- `docs/VALIDATION.md`
- `docs/OFFLINE.md`
- `docs/research/TEAM_CHARTER.md`
- `docs/research/TOKEN_BUDGET_POLICY.md`
- `docs/research/stages/stage-02/CHARTER.md`
- `docs/MASKING.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/EVALUATION.md`
- `docs/research/stages/stage-03/CHARTER.md`

## Confirmed decisions

- The first complete target is public-data `FlyTS-Mini v0.1`.
- The user is the final stage-gate authority.
- The default workflow is single-agent; specialists are activated selectively.
- Only the Research Director delegates; recursive delegation is prohibited.
- The primary Codex agent is the Research Director; it directly delegates to specialist subagents.
- `CURRENT_STATE.md` is the concise shared context, not a conversation transcript.
- Implementation and independent QA remain separate.
- Material ambiguity is `HOLD`: ask the user with options, recommendation, and impacts before continuing.
- User confirmation is required for changes to research direction, architecture, data/splits, metrics/acceptance, scope, budget, or confirmed decisions.
- Explicit "you decide" delegation is itself a user decision and must be recorded.
- QA independently re-runs relevant checks and writes only temporary or Git-ignored artifacts.
- The user approved the Stage 00 charter and execution plan with `GO` on 2026-09-24.
- The user approved the Stage 00 result with `GO` on 2026-09-24 after QA `PASS`; this closes Stage 00 and authorizes PR #6 merge, but does not begin Stage 01.
- The user approved the Stage 01 Charter and decision bundle with `GO` on 2026-09-24. Stage 02 remains separately gated.
- Stage 01 uses two-tier domain isolation, domain-macro masked Huber selection, 1/3/5 repetitions, ±5% parameter tolerance, optimizer-step compute matching, and Stage 03 numerical-threshold calibration.
- Stage 01 also fixes interpolation/extrapolation channel-count evaluation, target-local frozen probes, one diagnostic rerun, and single-factor attribution for topology, tokenizer, router, and backbone.
- The user approved paired unseen/seen count degradation, task-specific controlled frozen probes, paired masked-Huber topology endpoints, and Smooth L1 `beta=1.0` to resolve the Stage 01 QA hold.
- The user accepted the Stage 01 result and independent QA `PASS` with `GO` on 2026-09-24, closing Stage 01 and authorizing PR #7 merge without authorizing Stage 02.
- The user separately approved Stage 02's architecture and acceptance contract with `GO` on 2026-09-24; DEC-009 records the implementation boundary.
- The user accepted the Stage 02 result and final QA `PASS` with `GO` on 2026-09-25; DEC-010 closes Stage 02, leaves PR #8 for user-managed merge, and does not authorize Stage 03.
- PR #8 was merged into `main` at `461f1fc`; the user separately approved Stage 03 evaluator scope, deterministic fixtures, three 400-step development seeds, hierarchical bootstrap candidate, and the candidate-only threshold gate with `GO` (DEC-011).
- DEC-012 records the user's option A: train-only fitted preprocessing is retained; paired scoring uses a record-local common visible context reference frame. One extra bounded Implementation follow-up was approved for QA fixes and exact-hash public candidate evidence.
- DEC-013 records user `GO — defer freeze`: candidate evidence milestone accepted, numerical settings remain candidate, and additional evidence scope is a separate approval gate.
- DEC-014 records the user's closure path without numerical freeze: evaluator/candidate evidence accepted, final QA before closure, Draft PR creation authorized afterward, Stage 04 and merge separately gated.
- DEC-015 records independent final QA `PASS` and Stage 03 closure within the no-frozen-threshold scope; formal robustness pass/fail still requires separately approved reopened calibration and freeze.

## Open questions

- Whether the initial agent/model assignments need adjustment after real Stage 0 use.
- Whether a dedicated Research Ops agent is justified after pilot experiments begin.
- When suitable CUDA hardware will be available for the still-unverified GPU path.

## Active risks

- Dependency minimums are not fully pinned, so a future fresh install may resolve versions different from this run.
- The current environment has a CPU-only PyTorch build and no CUDA device; GPU behavior remains unverified.
- The foundation-model and topology-benefit claims remain unverified.
- Too many agents or full-lab reviews could waste tokens without improving evidence.
- Premature final-test access, post-hoc threshold selection, or unmatched multi-factor comparisons could invalidate later claims.
- Fully hidden channels cannot be distinguished without metadata; overlap and dropout require explicit target and statistic leakage checks.
- The approved public starter manifest is present locally with exact SHA-256 `e538e9cbf761577740f43f6930ac4653834fdc00f9d0ee567b02b52e2d0d14eb`; test and final-held-out arrays remain sealed.

## Latest evidence

- Initial PoC and foundation MVP PRs are merged.
- Development plan PR #3 is merged.
- Research-team governance PR #4 and human-alignment PR #5 are merged in `main` commit `9a6f3d8`.
- The user selected decision-gate checkpoints, mandatory clarification on ambiguity, and independent QA re-execution.
- The local research-governance validator passes for six specialist agents, two skills, the Stage 00 charter, and the shared notebook.
- The Stage 00 branch was created only after local `HEAD`, `origin/main`, and fetched remote `main` were confirmed equal at `9a6f3d8`.
- The project-local Python 3.12 environment contains PyTorch 2.14.0+cpu and pytest 9.1.1; the full suite passed with 24 tests and one CUDA hardware skip.
- The CPU smoke run completed two finite-loss epochs with 17,936 parameters; epoch-boundary resume reproduced all 29 model tensors bitwise and embedding export produced finite `[9, 32]` vectors.
- Independent QA reproduced the corpus split and hash, exact smoke losses, bitwise resume, embedding schema, full tests, and CUDA-unavailable classification. After the notebook refresh and validator rerun, QA issued `PASS`.
- PR #6 contains only the five Stage 00 evidence and governance documents, and its GitHub Actions test workflow passed before the result gate.
- The Stage 01 branch was created only after local `HEAD`, `origin/main`, and fetched remote `main` matched at `ad9655f`.
- The Stage 01 Charter records the approved scope, acceptance criteria, decisions, agent budget, user gates, and stop conditions without changing code, data, configuration, or model behavior.
- Program Integrator and Experiment Scientist completed non-overlapping read-only reviews with no material disagreement or request to change an approved decision.
- `PROJECT_CONSENSUS.md` and `EXPERIMENT_PROTOCOL.md` now map the approved domain, selection, budget, evaluator, attribution, and negative-result rules into Stage 2–10 handoffs.
- H-01–H-04, R-01–R-08, DEC-007, RK-08–RK-12, and the development checklist are aligned to the Stage 01 protocol; all scientific hypotheses remain `미검증`.
- Independent QA issued `FAIL` because unseen channel-count and frozen-probe evaluations lack complete primary metric/control contracts, H-03 lacks a prespecified topology claim endpoint, and the Huber transition parameter is not fixed.
- The approved remediation now specifies all four missing contracts in DEC-007, project consensus, experiment protocol, hypotheses, and requirements traceability; scientific results remain `미검증` until later stages.
- Independent QA revalidated the approved remediation and issued final `PASS`; notebook, governance, and diff validation also pass.
- Draft PR #7 (`https://github.com/yhlee52/FlyTS_lab/pull/7`) records the documentation-only scope, QA `PASS`, remaining limitations, and the approved integration path.
- Draft PR #7 GitHub Actions `tests` run #33 passed on commit `cbe483e` before the result gate.
- The user issued the Stage 01 result-gate `GO` after reviewing all acceptance results, QA, limitations, artifacts, and the Stage 02 boundary.
- Stage 02 implementation adds independent cause masks, nested configuration, visible-only pooled fallback, and focused tests; the result was accepted with user `GO`.
- The Stage 02 full CPU suite passes with two CUDA skips; the synthetic CPU smoke completed two finite-loss epochs with 17,936 parameters. Bitwise legacy and nested-config epoch resume, notebook/governance validators, and diff check pass.
- Initial Stage 02 independent QA issued `FAIL` for forced minimum channel targets, target-free single-channel handling, manual-plan validation, missing/padding distinction, charter completeness, records, and reproductions. The implementation follow-up removes the forced minimum, adds plan and padding checks, and preserves the initial QA verdict until re-review.
- After remediation, independent QA reproduced the corrected low-ratio sampling, invalid-plan rejection, missing/padding separation, target-free error, finite two-epoch CPU smoke, and 29-tensor bitwise resume, then issued final `PASS`.
- The full suite passes with 36 tests and two CUDA hardware skips; notebook/governance validators and diff check pass.
- PR #8 (`https://github.com/yhlee52/FlyTS_lab/pull/8`) was merged into `main` at `461f1fc`; its Stage 02 QA `PASS` remains the handoff basis.
- Draft PR #8 GitHub Actions `tests` run #40 passed on commit `3a25b46` after PR evidence links were added.
- The user issued the Stage 02 result-gate `GO` after reviewing implementation, compatibility, QA, risks, and unverified claims.
- Stage 03 is on `codex/stage-03-robustness-evaluator`. Public development calibration is complete; candidate QA issued a pre-remediation `CONDITIONAL PASS`, followed by remediation QA `PASS` for user-reviewable candidate evidence. The Charter `GO` covers evaluator and candidate generation only.
- The exact-hash public starter corpus passed development-only train/val verification without opening test arrays. Three 400-step CPU runs at seeds `7/17/29` used uniformly trained `last.pt`; each full evaluator run covered 522 validation windows, 38,634 raw rows and 31 metric arms with identical fixture/source hashes.
- `reports/robustness/calibration-candidate-v1.{json,csv,md}` records candidate-only control evidence and 10,000 paired hierarchical bootstrap intervals. Energy and transport each have one validation record; effect threshold freeze is not supported by independent controls.
- Experiment Scientist judged the candidate's reproducibility and aggregation structure suitable but numerical freeze unsupported. Independent QA issued a pre-remediation `CONDITIONAL PASS`; portable provenance, algebraic-reference wording, floor labels, and sparse count-arm coverage were corrected. Post-remediation implementation self-check passed, and independent remediation QA issued `PASS` for candidate review only. Threshold, guard and uncertainty freeze evidence remains insufficient.
- The user accepted the candidate evidence milestone with `GO — defer freeze`; this did not authorize additional evidence work or Stage 03 closure.
- The user subsequently approved Stage 03 closure without numerical freeze and a Draft PR after final QA. Independent final QA reported `PASS` for all eight Charter criteria in that bounded scope; `RESULT.md` is closed. Robustness pass/fail and final claims remain prohibited.

## Next action

Let the Research Director prepare the authorized Stage 03 Draft PR for review. Merge requires separate user approval. Do not freeze numerical settings or start Stage 04 without a separate gate.
