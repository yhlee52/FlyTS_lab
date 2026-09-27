# Stage 08 Independent QA Report

Status: **PASS — final DEC-030 code QA**

Date: 2026-09-27

## Scope

Independent read-only review of the Stage 08 implementation and the four-arm
`1 + resume + 1` preflight under
`outputs/stage08-pilot/preflight-20260927-rerun1/`. The initial runner-defect
evidence remains preserved under `outputs/stage08-pilot/preflight-20260927/`.

## Passing evidence

- All four core arms completed two finite epochs through a real process-boundary
  resume, with two optimizer steps, 16 samples and the approved parameter counts.
- Independent recomputation matched every best, last and pre-resume checkpoint
  hash. The common Bike fixture matched across arms; recorded evaluation is
  Bike-only and seen channel counts are the pretrain counts 11 and 26.
- Development verification excludes final-held-out records before array loading.
  QA did not open Electricity arrays.
- Nine focused tests, the full suite with three CUDA skips, report byte check,
  notebook/governance validators and `git diff --check` passed.

## Initial blocking findings

1. `tools/run_stage08_pilot.py` binds package sources but not the runner, report
   generator or pilot manifest. `tools/report_stage08_pilot.py --check` verifies
   four output artifacts but does not independently recheck the recorded source,
   config, manifest, registry and fixture bindings. This does not satisfy the
   exact-provenance acceptance criterion.
2. Stage 09 scenario accounting combines setup and validation and omits a distinct
   checkpoint cost. Preflight estimates are correctly unavailable because a
   one-step segment has no steady post-warmup measurement, but the real-pilot
   reporter still cannot separate setup, validation, checkpoint and evaluation.

## DEC-028 remediation re-review

Status: **FAIL**

The initial source/config binding and cost-phase findings are substantially
remediated. Schema-v2 facts now bind the Stage 08 tools, configs, package sources,
inputs, evaluation fixture/records, checkpoints and resource files. The reporter
rehashes those inputs, and setup, training-step, validation, checkpoint and
evaluation phases remain distinct. Focused Stage 08 tests and notebook/governance
validation pass.

Two blockers remain:

1. The reporter does not derive `optimizer_steps`, sample exposure or parameter
   count from bound resource/checkpoint/config evidence. QA changed only the
   synthetic run fact from two steps to 999 and the report accepted it.
2. The full suite has one failure: the Stage 07 byte-stability test asks the old
   generator to hash current Stage 08-modified training/evaluation sources against
   the correctly frozen Stage 07 report. The archival evidence must remain
   unchanged, but the stale cross-stage check must be made archival-aware.

Schema-v2 correctly rejects the immutable schema-v1 preflight. No schema-v2 public
preflight or pilot was run. CUDA remains skipped.

## Gate

The separate pilot-run gate remains `HOLD`. A further Implementation follow-up and
independent QA re-review require another explicit agent-budget exception. After the
two blockers pass, the PI must decide whether the historical schema-v1 preflight is
sufficient operational evidence or authorize one new common schema-v2 preflight.
The 400-step core runs, 20-step dense diagnostic, measured cost scenarios, OOM
behavior and tracked pilot reports remain unverified.

## DEC-029 remediation re-review

Status: **FAIL**

The execution-fact blocker is closed. Schema-v2 now derives and cross-checks
segment step counts, optimizer counters, epoch configs and histories, earliest-best
selection, total optimizer steps, sample exposure and expected parameter metadata.
Negative tests reject five altered execution facts. Focused tests (19), the full
local suite with three CUDA skips, validators and `git diff --check` pass.

One blocker remains. The Stage 07 archival test calls `git show 34b83c2:<path>`.
GitHub Actions uses the default shallow `actions/checkout@v4`, so that historical
object is not guaranteed after a Stage 08 commit; an offline source snapshot also
lacks it. Replace the history lookup with a self-contained immutable byte check
without changing either Stage 07 report. Their current exact SHA-256 values are:

- JSON: `76a5f906201fb03415ebd078dbc963d23cb6a00bfb3ff43c7ff7781502b39ecb`
- Markdown: `0f6d53338652da14469f9b7146314ab23c94ff2ba05df9ce5381fc140b127dc4`

The preflight-versus-pilot PI gate remains premature until this final code QA
blocker is corrected and independently rechecked.

## DEC-030 final re-review

Status: **PASS**

The Stage 07 archival test now reads only the two frozen reports and checks their
exact SHA-256 values. It requires no Git history or network and works in shallow or
offline source snapshots. The report bytes and Stage 07 QA evidence are unchanged.

Schema-v2 execution-fact cross-checks and tamper rejection remain intact. Focused
tests (19), the full suite with three CUDA skips, compile of 46 Python files,
notebook/governance validation, `git diff --check` and Git-ignore checks pass.

No schema-v2 public preflight or pilot was run. Code QA has no remaining blocker;
the PI must now choose whether the preserved schema-v1 four-arm preflight is
sufficient for the operational gate or authorize one common schema-v2 preflight.
QA recommends the new schema-v2 preflight because it exercises the exact current
provenance and phase-accounting path on public data.

## DEC-032 post-pilot independent QA

Status: **PASS**

The canonical fixed-order run contains five separate arm directories and two real
training processes per arm. All 15 best, last and preserved resume-input hashes
match. The four core arms each record 400 optimizer steps and 3,200 samples with
approved parameter counts; dense remains diagnostic-only at 20 steps and 160
samples. Configs, seeds, masking, optimizer, CPU conditions, windows and pretrain
domains match, and every saved history is finite.

Each saved `L_select` is the equal mean of the Appliances and Beijing domain losses.
Epoch 2 is the earliest minimum for every arm and is the checkpoint evaluated on
Bike. Bike is the only evaluation domain; all arms share the same fixture hash and
use pretrain seen channel counts 11 and 26. Development verification excludes
final-held-out records before array loading. QA did not access Electricity arrays.

The strict schema-v2 report `--check` reproduced both tracked reports byte for byte
from the resolved absolute run path and independently verified source, config,
input, checkpoint, resource, evaluator-record and fixture bindings. Resource phases
remain separate, and Stage 09 cost scenarios are labeled linear estimates. The
report makes no winner, significance, robustness pass/fail or Bike-driven selection
claim.

Focused tests passed (19); the full suite passed with three CUDA skips. Compilation
of 46 Python files, notebook/governance validation, `git diff --check` and Git-ignore
checks passed. Raw outputs and data remain ignored and Stage 07 evidence is
unchanged. QA did not rerun the pilot or trace historical filesystem opens.
Record-level target sums are not separately persisted, so aggregation was checked
through code/tests and saved domain histories. Rewired setup cost and all Stage 09
extrapolations remain single-run CPU observations, not comparative efficiency.

No blocker remains for the PI Stage 08 result gate.
