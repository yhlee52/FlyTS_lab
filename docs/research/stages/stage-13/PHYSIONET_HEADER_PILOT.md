# PhysioNet EEG v1.0.0: six EDF headers

Status: bounded header-schema screen under PI `GO` DEC-085, 2026-10-11.
Source/use, role, split and H-01 held-out count endpoint: **HOLD**. This is
not an admitted corpus or a protocol-v3 result. Independent
[documentation/method QA](PHYSIONET_HEADER_PILOT_QA.md): **PASS**, without
EDF-byte replay. The access [request](PHYSIONET_HEADER_PILOT_REQUEST.md) had
independent document-only QA `PASS` before any EDF read.

## Authorization, method and provenance

The six exact paths were fixed in the request from the approved
[RECORDS](https://physionet.org/files/eegmmidb/1.0.0/RECORDS) sidecar: S001,
S055 and S109, each R01 and R03. The publisher's [dataset page](https://physionet.org/content/eegmmidb/1.0.0/)
describes 64 EEG channels at 160 Hz and EDF+ files. The pilot tested header
structure against that description, without selecting files by values or
performance.

On Windows 10 with Python 3.14.5 `urllib.request` (standard library), at Git
base `4209994cb3cf`, the Director sent `Accept-Encoding: identity` and exact
HTTP byte-range requests to `https://physionet.org/files/eegmmidb/1.0.0/`.
Redirects were disabled. Each response had to be HTTP 206, the same official
URL, exact `Content-Range` start/end/total and `Content-Length`, and no
non-identity content encoding. The first request read bytes 0–255; its EDF
header-length field then fixed the second range 256–(header length−1).
Header length had to equal `256 × (1 + signal_descriptors)` and fit the
32 KiB cap. The stream read at most the exact accepted range length and was
closed without a sample-byte read. A separate initial 256-byte probe of
S001R01 was also within that file's total cap.

No EDF or raw header bytes were saved. The interpreter inspected only EDF
header fields: length, signal labels, samples per record, record duration and
record count. It did not print patient/recording identifiers or start dates.
The six response `Content-Range` totals below are server-declared file sizes,
not verified file hashes. Total header bytes read in this pilot were 101,632;
maximum for one file was 17,152 bytes (S001R01 including the probe).

## Observed header fields

| Path | HTTP total bytes declared | Header bytes | EDF descriptors | EEG labels | Annotation descriptors | EEG rate | Header-declared duration |
|---|---:|---:|---:|---:|---:|---:|---:|
| `S001/S001R01.edf` | 1,275,936 | 16,896 | 65 | 64 unique | 1 | 160 Hz | 61 s |
| `S001/S001R03.edf` | 2,596,896 | 16,896 | 65 | 64 unique | 1 | 160 Hz | 125 s |
| `S055/S055R01.edf` | 1,275,936 | 16,896 | 65 | 64 unique | 1 | 160 Hz | 61 s |
| `S055/S055R03.edf` | 2,555,616 | 16,896 | 65 | 64 unique | 1 | 160 Hz | 123 s |
| `S109/S109R01.edf` | 1,255,296 | 16,896 | 65 | 64 unique | 1 | 160 Hz | 60 s |
| `S109/S109R03.edf` | 2,555,616 | 16,896 | 65 | 64 unique | 1 | 160 Hz | 123 s |

All six headers had a one-second data-record duration and the same ordered
64 EEG labels. The SHA-256 of the 64 stripped label strings joined with LF
was `408d6576054f7ae71c71fbd35f35d63341a2a436b4d63f254fb733f8f161dc46`
for each. This is a **header-label digest**, not a raw EDF or manifest hash.
An EDF annotation descriptor was identified by its label; annotation values
and `.edf.event` contents were not read or used for H-04.
For each file, `(HTTP total bytes − 16,896) / header data-record count` equals
20,640 bytes per record, an internal size-field consistency check only.

## What this screen can and cannot support

The six predetermined headers are consistent with 64 similarly ordered,
nominal 160 Hz EEG channels in three listed subject IDs and two run numbers.
They reduce schema risk for a possible 11/26/>26 channel-count audit. They do
not establish actual signal validity, missingness, common observed targets,
paired nested views, original-subject independence, cross-subject variation,
rights/notice compliance, or a leakage-safe group/time split. Durations above
are header declarations; no sample count or sample value was independently
checked against the full files. The other 1,520 EDF headers were not accessed.

The [sidecar inventory](PHYSIONET_SIDECAR_AUDIT.md) and this screen do not
admit PhysioNet for development or authorize a split. A separately scoped
source/use, role and split packet is required before any broader source
access. Stage 13 full protocol-v3 freeze and Q1 claims remain `HOLD`; H-04
remains `not tested`, Q2/Q3 unavailable. Electricity/test signals/scores stayed
sealed; Stage 09 `HOLD`/QA `FAIL` and DEC-070 release `STOP` are unchanged.
