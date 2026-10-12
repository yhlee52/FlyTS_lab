# Stage 14 Draft PR automatic CI boundary

Status: **incident recorded; no Stage 14 execution evidence**.

The repository's preexisting `.github/workflows/test.yml` runs pytest, creates
a synthetic corpus and performs a CPU pretrain smoke on every push and PR. The
Director pushed static Stage 14 preparation to Draft PR #37 before excluding
that branch from this automatic model path. This conflicted with DEC-114's
separate exact-run gate. No Stage 14 opt-in runner or cases executed, and no
real data, Electricity or test signals were read by the declared CI commands.

GitHub Actions runs `38257295861` and `38257304875` on `ed4933b` completed
the existing pytest, synthetic and CPU pretrain smoke steps before cancellation
was requested. Runs `38257689365` and `38257693326` on `4b7878a` reached
pytest; cancellation skipped their separate synthetic and pretrain steps.
The pytest suite itself may execute preexisting synthetic model tests. These
results and any transient CI checkpoints are **unapproved for Stage 14** and
must not enter the Stage 14 manifest, result, Q0 claim or formal evidence.
CI artifacts were not inspected. The Director requested cancellation of all
four runs upon finding the workflow boundary and stopped further pushes until
the branch guard was prepared.

The workflow now routes this named Draft PR branch to governance and AST-only
checks; its ordinary pytest/synthetic/pretrain job is skipped for both push
and pull-request events on that branch. This branch-specific control is not a
general network sandbox or a substitute for independent pre-execution QA.
Changing the branch name or removing the guard requires a fresh gate review
before another push. Formal Stage 13 remains HOLD; the exact Stage 14 manifest,
CPU resource cap, independent pre-execution QA and PI run GO remain pending.
