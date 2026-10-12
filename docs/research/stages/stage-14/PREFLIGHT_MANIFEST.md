# Stage 14 engineering preflight — exact-run packet (draft)

Status: **static preparation only; no execution approval**. DEC-114 approved the
engineering Charter, not this packet, a resource cap, model tests or a CPU run.
Formal Stage 13 remains `HOLD`; this packet cannot serve as protocol v3 or a
formal Stage 14 handoff.

## Proposed synthetic command

The opt-in entry point is `tools/stage14_preflight.py --run`. It refuses to run
without `configs/stage14/approved_preflight.json` and an environment variable
containing the PI-approved raw-byte SHA-256 of that exact JSON. The command
validates the manifest and tracked input bytes before model import or output
creation. It uses the historical *unfrozen* Stage 09 matrix only to select four
synthetic fixture rows: 0, 15, 30 and 45. The resulting four arm observations
are mechanics checks, not four formal runs or scientific evidence. The opt-in
`tools/stage14_preflight_cases.py` cases are outside pytest's automatic `tests/`
collection and also wait for the exact execution decision.
The PR branch uses a [static-only CI guard](CI_BOUNDARY.md); earlier automatic
CI smoke runs are excluded from Stage 14 evidence.

Only generated toy arrays and same-run resume checkpoints may be read. The
allowlist includes the Stage 09 matrix, role registry, source modules and the
preflight tools; it excludes `data/`, preexisting `outputs/`, Electricity and
test paths. Outputs go to ignored `outputs/stage14/preflight/`; an existing
output directory stops the run. A Git commit and raw-byte hashes bind inputs.
The registry's canonical LF bytes must match; a CRLF worktree fails closed.
`.gitattributes` pins LF checkout for every declared text input and is itself
hashed. Existing Windows worktrees may still contain CRLF until those files
are rechecked out; pre-execution QA must inspect raw worktree bytes and stop
on any difference. This rule changes no historical registry or matrix blob.

## Exact fields required before independent pre-execution QA

| Field | Current status and completion rule |
|---|---|
| Code commit and input hashes | **Pending** final static code review and commit. Generate from that commit, then verify worktree bytes before QA. Do not rewrite historical manifest or registry hashes. |
| Python/dependency lock | **Pending runnable environment.** The currently selected local Python is 3.14.5 and lacks NumPy and PyTorch; no local venv is present. Record exact Python executable/version and installed distribution versions only in the chosen offline CPU environment. |
| CPU identity and limits | **Pending.** Pin platform, machine, processor, logical CPU count, float32, one thread, a timeout, observed peak RSS bound and output disk bound. Obtain the PI's exact numerical approval before any model test or smoke. |
| Commands and fixture | Pin the one opt-in command, four rows, seed 7, prepared adversarial cases and the exact stdout/stderr/output hash ledger contract. Seed 7 is an existing synthetic fixture selector, not a formal seed freeze. |
| Network and process isolation | Python socket denial is proposed for child interpreters, but it is not universal network isolation. Confirm child process tree timeout handling and decide whether an OS network block is needed before QA. |
| Resource enforcement | The proposed per-row RSS and disk checks are observations after a row. They cannot guarantee a strict live memory/disk ceiling. The exact packet must present this limitation and a conservative host capacity or stronger controls to the PI. |
| QA and PI gates | Independent pre-execution QA must review this **completed** packet, exact byte hashes, guards and process boundaries. Only then may the PI approve that exact manifest SHA-256, CPU cap and one execution. |

No numerical timeout, memory, disk or wall-time estimate is asserted here.
The initial Charter's conditional document QA is not a pre-execution verdict.

## Stop and interpretation rules

Missing or mismatched manifest, dependency, code/registry bytes, undeclared
input, preexisting output, network-guard failure, child timeout, reporter
replay mismatch, or observed resource overrun stops the single run. A failed
attempt remains in the ledger; no automatic retry or alternate row selection.
The packet must state any limits of failure capture after a process-tree kill.
No `GO` for model tests, synthetic execution, checkpoint creation, Stage 15,
CUDA, data admission, formal H-01–H-04 or public release follows from this
static draft. Q0 is the maximum possible engineering label after later QA.
