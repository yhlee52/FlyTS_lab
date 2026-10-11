# Proposed next PI gate: six PhysioNet EDF headers

Status: approved by PI as DEC-085 and performed within the stated scope; see
the [header pilot result](PHYSIONET_HEADER_PILOT.md). This request followed
the DEC-084 sidecar inventory and its independent QA `PASS`. The request
itself received independent document-only QA `PASS` after a range and byte-cap
correction; QA was not the access authority.

## Proposed bounded read

Read the EDF+ **header bytes only** for these six publisher-listed paths:

| Subject ID selected before data values | Baseline run | Task run |
|---|---|---|
| First listed, S001 | `S001/S001R01.edf` | `S001/S001R03.edf` |
| Middle listed, S055 | `S055/S055R01.edf` | `S055/S055R03.edf` |
| Last listed, S109 | `S109/S109R01.edf` | `S109/S109R03.edf` |

Selection uses only lexicographic subject IDs and run numbers from the
approved `RECORDS` sidecar, never signal or performance. Request a 256-byte
HTTP range for each fixed EDF header, read its declared header length, then
request only the remaining header bytes `256-(header_length-1)` (no second
request if the header is exactly 256 bytes), with a 32 KiB total per-file cap.
Require HTTP 206 and an exact `Content-Range` of `bytes 0-255/T` on the first
response and `bytes 256-(header_length-1)/T` on the second, with the same `T`.
Reject redirects away from `physionet.org`. Hard-stop the stream if received
bytes exceed 256 initially or `header_length-256` on the second read. If the
server ignores a range or the header length is below 256 or above 32 KiB,
stop that file without reading a full EDF. Keep bytes in memory
for schema inspection only; do not write a local EDF.

The permitted checks would be header length, signal count and names, EDF+
annotation-channel distinction, per-signal sample counts, record duration,
declared start time and basic consistency across these six files. This is a
**screen** for whether a larger audit is worth requesting. It is not a check
of signal samples, missingness, full subject inventory or paired observed
targets. A six-file pilot cannot establish source-wide validity or a safe
subject-disjoint split.

The request excludes all sample bytes, `.edf.event` or annotation contents,
full files/archive, local download, preprocessing, role/split changes,
training, evaluation, Electricity and all sealed test signals/scores. If the
PI approves this header pilot, source/use admission, role and split still
require later distinct PI decisions. If the PI instead wants a full-source
audit proposal, estimate its I/O and storage before seeking that broader
access. The publisher page currently lists about 1.9 GB compressed and
3.4 GB uncompressed for the resource; no local cost has been measured.

## Decision options

The PI selected option 1 (`GO`, DEC-085) on 2026-10-11. The alternatives below
are preserved as the reviewed request, not active approvals.

1. **GO, recommended:** authorize only the six header reads above. Low data
   exposure screens channel/time compatibility, but H-01 count stays `HOLD`.
2. **REVISE:** request a separately costed broader source-audit proposal;
   no EDF read begins under this option.
3. **HOLD:** stop PhysioNet access and leave source admission/protocol freeze
   pending; the existing PAMAP2 and Daily/Sports shortlists remain unadmitted.

No option here admits an H-04 target, changes DEC-070, or unseals Electricity
or test data. Stage 09 records and hashes remain unchanged.

## Independent request QA

An independent reviewer confirmed that all six fixed paths occur in the
approved `RECORDS` sidecar. Their initial review found that HTTP 206 alone
would not prove the returned byte range or cap. The request now specifies
exact `Content-Range` and stream-length checks, same total-file length across
both requests, and official-host restriction. The reviewer returned `PASS`
on the revised request. No EDF was accessed in this review.
