# PhysioNet EEG v1.0.0: approved sidecar inventory

Status: filename/checksum-list inventory only; independent sidecar QA **PASS**
([review](PHYSIONET_SIDECAR_QA.md)); proposed source/use, role and split:
**HOLD**. Read on 2026-10-11 under the PI's sidecar-only access `GO`
(DEC-084). This is not candidate admission or an H-01 endpoint validation.

## Exact access and provenance

Only the official publisher's [RECORDS](https://physionet.org/files/eegmmidb/1.0.0/RECORDS)
and [SHA256SUMS.txt](https://physionet.org/files/eegmmidb/1.0.0/SHA256SUMS.txt)
were read through their rendered plain-text web views. The [dataset landing
page](https://physionet.org/content/eegmmidb/1.0.0/) identifies both sidecars
as version 1.0.0 files and displays sizes of 25.3 KB and 253.8 KB. The page
reports Open Data Commons Attribution License v1.0;
use obligations and any bundled notices still need source-admission review.

The web views supplied text and line indices, not byte-exact source streams.
No local copy or raw-byte SHA-256 of either sidecar was produced. In particular,
the publisher's digest for `RECORDS` below was **read**, not independently
verified. Retrieval bytes, member bytes, archive hashes and notice contents
remain `unverified`. No download into `data/` occurred.

## Inventory results

| Check | Observed from approved sidecars | Limit |
|---|---|---|
| `RECORDS` syntax and count | 1,526 distinct paths of the form `S###/S###R##.edf`; subject folder and filename IDs agree. IDs S001–S109 each list R01–R14, once each. | This is a listed-file count: 109 subject IDs × 14 run names. It is not 1,526 independent subjects or proof that the EDF bytes exist and are usable. |
| Publisher checksum list | 3,058 distinct, syntactically valid `64-hex-digest path` rows: 1,526 `.edf` paths, their 1,526 `.edf.event` companion paths, and six ancillary paths. All `RECORDS` EDF paths and their expected `.event` names occur once. | Digest values are publisher declarations. No EDF or `.event` member bytes were fetched or checked. Checksum-list order is not record order. |
| Six ancillary checksum paths | `RECORDS`, `ANNOTATORS`, `wfdbcal`, `64_channel_sharbrough.pdf`, `64_channel_sharbrough.png`, `64_channel_sharbrough-old.png`. | Only names and published digests were read; ancillary file contents were not opened. |
| Published `RECORDS` digest | `02d1de9c00511d3b7548a6b59bdf209c819db025518ddcc52b21fd3b2b9de4a8`. | Not independently recomputed from raw bytes. `SHA256SUMS.txt` has no self-hash entry in its listed rows. |

The inventory was checked by parsing every rendered line of each authorized
plain-text view, rejecting malformed path/digest syntax or duplicate paths,
and comparing each of the 109 × 14 expected EDF and `.edf.event` names against
the checksum list. This verifies **list agreement**. It does not verify
published digest values, signal semantics or subject independence.

## Eligibility impact and next access decision

The filename inventory supports a plausible subject-group structure for a
future held-out H-01/H-02 audit. It does not establish that each EDF contains
64 genuine aligned observed channels, stable cadence, valid lengths or masks,
nor that an 11/26/>26 same-record nested view has a common target/reference.
Actual subject identity and collection dependence, split-before-windowing,
purge, train-only preprocessing, rights/notice compliance and raw-byte hashes
are also unverified. Runs and windows within a subject are dependent. No
source/use, development role, train/validation/test split or seal is decided.

A further PI decision would have to name the exact source access and cost
before any EDF header, signal, `.event`, archive or download is attempted. The
publisher lists approximately 1.9 GB compressed and 3.4 GB uncompressed for
the full resource; these are planning figures, not measured local I/O. A
minimal next option is a predetermined, header-only sample across selected
subject/run IDs to screen channel layout and duration without reading signal
samples. A fuller audit would need separately authorized source bytes and a
precommitted subject-disjoint split proposal. Neither option is approved by
DEC-084. The separate [six-header request](PHYSIONET_HEADER_PILOT_REQUEST.md)
defines the proposed pilot and awaits PI decision. H-01 held-out count and
protocol-v3 freeze remain `HOLD`.

Electricity and all test signals/scores stayed sealed; no annotation content,
array, model score, training or evaluation was accessed. HAR/HARTH remain
`HOLD`, H-04 `not tested`, Stage 09 `HOLD`/QA `FAIL` unchanged and DEC-070
public-release `STOP` remains in force.
