# Proposed PhysioNet eligibility signal audit: separate PI gates

Status: **draft for review only**. DEC-085 permitted six EDF headers, not signal
bytes or full-file transfer. No signal or annotation value has been read.
Source/use admission, development role and formal split remain `HOLD`.

## Why another access is needed

The [six-header pilot](PHYSIONET_HEADER_PILOT.md) found 64 named EEG channels
at a header-declared 160 Hz in three listed subject IDs. It cannot establish
that the channels contain valid, simultaneous observations or that an
11/26/>26 nested view has a common observed target. The original H-01 count
endpoint and protocol-v3 freeze therefore remain `HOLD`.

The [official resource](https://physionet.org/content/eegmmidb/1.0.0/) is
marked open access and ODC Attribution v1.0. Its [linked license text](https://physionet.org/content/eegmmidb/view-license/1.0.0/)
states attribution/notice conditions for public conveyance and distinguishes
database rights from possible rights in individual contents. Publisher status
supports a *request for internal eligibility audit*; full source/use and any
publication/redistribution decision remain separate PI gates. Preserve the
publisher citation, license link and exact member hashes in a later admission
packet. This is a screening inference, not rights clearance. No source data or
derived array belongs in public Git.

## Named source access proposal

Only the six files already named before signal access are candidates:
S001/S001R01, S001/S001R03, S055/S055R01, S055/S055R03, S109/S109R01 and
S109/S109R03, all `.edf` under the official v1.0.0 `/files/` path. Their
HTTP-header-declared sizes sum to **11,515,296 bytes (10.98 MiB)**. This is
the maximum planned full-file network transfer, excluding HTTP overhead; it
is not a measured download or Stage 13 compute envelope. The largest single
file is 2,596,896 bytes. Use only bounded in-memory reads; save no EDF or raw
array, and retain only hashes, channel-quality counts and eligibility flags.

Two mutually exclusive technical access scopes are offered for PI choice:

| Scope | Exact access and consequence |
|---|---|
| A — six full EDF streams | Transfer each complete file in memory, verify its SHA-256 against the publisher sidecar, parse only the 64 EEG channels. EDF+ annotation bytes necessarily transit with each file, but are neither decoded nor retained. Do not open `.edf.event`. Six HTTP file requests; about 11.5 MB of source bytes. |
| B — EEG-only byte ranges | Re-read only the six headers and the EEG sample spans for the 553 header-declared one-second records. Verify exact HTTP ranges and stop if EEG channels are not contiguous before the annotation descriptor. No annotation sample bytes are transferred. Approximately 11.33 MB of EEG bytes plus headers, but at least 553 range requests and no complete member SHA-256 verification. |

Neither scope permits annotation *use*, event labels, an H-04 task, model
predictions/losses, training, performance-ranked channels/subjects, local
source download, archive access, Electricity or any sealed test signal/score.
Scope A is recommended for hash verification and much lower request overhead;
its unavoidable annotation-byte transit is disclosed for the PI to accept or
reject. If neither scope is acceptable, keep this source on access `HOLD`.

## Proposed audit-only role and split restriction

Before either signal scope, the PI must separately decide that S001, S055 and
S109 are **audit-only subjects**, excluded from encoder pretraining, formal
development evidence and any sealed/final test. The other 106 listed IDs stay
unassigned. This is a narrow future-test exclusion, not admission of the
dataset, a full subject split or permission to inspect any remaining subject.
It prevents the six signal-inspected files from later masquerading as blind
test data. No subject ID is chosen from scores or coverage; all six paths were
fixed from the sidecar before any signal access.

Within the approved audit-only subset, the bounded checks would be member
digest match (scope A), EDF parse consistency, actual sample count and cadence,
per-channel finite/nonfinite counts and zero distinction, simultaneous
observed coordinates, and whether nested 11/26/64 channel views can share
the same observed target/reference. Report only source-quality metadata and
eligibility. Do not calculate model errors or choose a protocol endpoint.
Failure, missingness or discordant hashes are reported, not used to substitute
new subject IDs after viewing outcomes.

## Staffing and stop conditions

Data specialist review and independent QA are proposed only if the separate
[specialist-budget amendment](AGENT_BUDGET_REVISION_REQUEST.md) receives PI
`GO`. Without that amendment, the Director may draft but does not claim
independent source QA or source admission. Even with staffing, no access starts
until the PI decides both the exact access scope and audit-only restriction.

Stop on off-host redirect, size/hash mismatch, unexpected annotation layout,
invalid EDF parse, any test/seal ambiguity or out-of-scope byte access. Any
broader source collection, role, split or source/use admission needs its own
reviewed PI packet. Stage 09 `HOLD`/final QA `FAIL` and report hashes, H-04
`not tested`, and DEC-070 public-release `STOP` remain unchanged.
