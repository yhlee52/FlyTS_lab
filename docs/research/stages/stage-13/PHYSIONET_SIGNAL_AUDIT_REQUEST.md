# Proposed PhysioNet eligibility signal audit: separate PI gates

Status: **scope A access `GO` (DEC-087) and audit-only exclusion `GO`
(DEC-088)**, with independent
[document-only QA `PASS`](PHYSIONET_SIGNAL_AUDIT_REQUEST_QA.md).
No signal or annotation value had been read before these two decisions.
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
publisher DOI citation, original-paper citation, license link, ODC attribution
notice and exact member hashes in a later admission packet. Database rights do
not by themselves clear rights or privacy obligations in individual EEG
contents. This is a screening inference, not rights clearance. No source data
or derived array belongs in public Git.

## Named source access proposal

Only the six files already named before signal access are candidates:
S001/S001R01, S001/S001R03, S055/S055R01, S055/S055R03, S109/S109R01 and
S109/S109R03, all `.edf` under the official v1.0.0 `/files/` path. Their
HTTP-header-declared sizes sum to **11,515,296 bytes (10.98 MiB)**. This is
the maximum planned full-file network transfer, excluding HTTP overhead; it
is not a measured download or Stage 13 compute envelope. The largest single
file is 2,596,896 bytes. For scope A, require HTTP 200 and the exact
header-pilot file size as both the expected HTTP `Content-Length` and hard
per-file receive cap; never read beyond that cap, and abort on a declared
overlength or early EOF. The client cannot establish whether a nonconforming
server has trailing, undeclared bytes without exceeding the approved cap;
the official member SHA-256 must also match. Both scopes use the official exact URL
only, reject redirects or content encoding other than identity, and require
the expected HTTP status and response length before reading. Use only bounded
in-memory reads; save no EDF or raw array, and retain only provenance
metadata, hashes and fixed channel-quality counts/flags.

Two mutually exclusive technical access scopes are offered for PI choice:

| Scope | Exact access and consequence |
|---|---|
| A — six full EDF streams | Transfer each complete file in memory, verify its SHA-256 against the publisher sidecar, parse only the 64 EEG channels. EDF+ annotation bytes necessarily transit with each file, but are neither decoded nor retained. Do not open `.edf.event`. Six HTTP file requests; about 11.5 MB of source bytes. |
| B — EEG-only byte ranges | Re-read only the six headers and the EEG sample spans for the 553 header-declared one-second records. Require HTTP 206, exact `Content-Range` start/end/total and `Content-Length`, identity encoding, and a hard cap equal to each requested range; stop if EEG channels are not contiguous before the annotation descriptor. No annotation sample bytes are transferred. Exactly 11,325,440 EEG bytes plus 101,376 header bytes are planned; the two-range header procedure plus per-record EEG spans requires at least 565 range requests (12 header + 553 signal), with no complete member SHA-256 verification. |

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
The six EDFs represent three subject groups with repeated runs, not six
independent entities. This pilot cannot establish cross-subject independence,
statistical power or H-01 generalization. Any later source split must group
by subject before windowing; runs and windows stay inside their subject
partition and never cross recording boundaries.

Within the approved audit-only subset, the bounded checks would be member
digest match against the publisher sidecar (scope A), EDF descriptor order,
units and digital-to-physical scaling, per-channel sample counts, record
duration, full-file length, payload/sample-count consistency with the
header-declared cadence, and annotation-channel
exclusion. Record official source/version/member URL, retrieval date and
digest verification method; the earlier sidecar inventory did not verify
member bytes. Count finite/nonfinite digital or scaled samples, exact zeros
and digital-rail hits separately per channel and per run. Do not treat zero as
missing or infer an undocumented missing sentinel. Fixed mechanical flags
are: header or record-length inconsistency, nonfinite scaling result, digital
sample outside its declared digital minimum/maximum, and a channel with zero
simultaneously observed coordinates in a requested nested view. Report each
flag and count without an after-values threshold or channel exclusion rule;
any eligibility decision waits for a reviewed packet and separate PI gate.
Apply no imputation or channel selection based on quality.
Assess simultaneous observed coordinates and whether header-order nested
11/26/64 channel views can share the same observed target/reference, without
choosing a final endpoint. Report only source-quality metadata and
eligibility, including any invalid flags and subject/run counts. Do not
calculate model errors or choose a protocol endpoint.
Failure, missingness or discordant hashes are reported, not used to substitute
new subject IDs after viewing outcomes.

## Staffing and stop conditions

DEC-086 approved the separate
[specialist-budget amendment](AGENT_BUDGET_REVISION_REQUEST.md). Data specialist
review of this proposal and independent QA passed before PI access decisions.
The reviews themselves did not admit the source. The PI separately approved
scope A and the audit-only restriction in DEC-087/088; scope B is not approved.

Stop on off-host redirect, size/hash mismatch, unexpected annotation layout,
invalid EDF parse, any test/seal ambiguity or out-of-scope byte access. Any
broader source collection, role, split or source/use admission needs its own
reviewed PI packet. Stage 09 `HOLD`/final QA `FAIL` and report hashes, H-04
`not tested`, and DEC-070 public-release `STOP` remain unchanged.
