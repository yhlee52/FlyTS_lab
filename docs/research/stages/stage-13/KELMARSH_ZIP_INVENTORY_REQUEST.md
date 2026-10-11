# Proposed minimum-byte Kelmarsh ZIP inventory gate

Status: **proposal only**. The PI selected recovery route A (DEC-102), which
preserves the Stage 11 H-01–H-03 contract. That decision does **not** approve
this source-file read, independent QA expansion, source/use admission, a
development role or a split. The Stage 13 freeze remains `HOLD`.

## Exact first unit

The [Cubico Kelmarsh v4 owner record](https://zenodo.org/records/16807551)
lists its smallest annual SCADA ZIP as `Kelmarsh_SCADA_2016_3082.zip`. The
[official record metadata](https://zenodo.org/api/records/16807551) reports
exactly **97,915,553 bytes**, publisher MD5
`ca8efbb6dbcfae3516583937eb5b5402`, and this exact content URL:

`https://zenodo.org/api/records/16807551/files/Kelmarsh_SCADA_2016_3082.zip/content`

The first proposed source read is **one HTTP GET Range** for the last
**131,072 bytes only**, `bytes=97784481-97915552`. The application-read cap
is **131,072 bytes total**, with no retry or fallback to a full download.
Require HTTP 206, exact final URL, `Content-Range:
bytes 97784481-97915552/97915553`, exact `Content-Length: 131072`, and
identity encoding before reading the body. HTTP 200, redirect, changed size,
short response or missing/invalid ZIP directory stops the attempt at `HOLD`.
The script does not try a second range if the directory exceeds the cap.

Parse only the ZIP end and central directory. Emit at most 128 member names,
compressed/uncompressed byte counts, compression methods, encryption flags,
CRC-32 values, response byte count and tail SHA-256. Do not open a member or
emit a CSV header, timestamp, measurement, event, array or score. Keep the
tail in memory and save no source bytes. The publisher MD5 covers the **whole
archive** and cannot be verified from this tail; `Content-Range` and tail
SHA-256 are bounded provenance, not source identity proof. Transport-layer
buffering beyond application reads is not measured.

The tool is `tools/stage13_kelmarsh_zip_inventory.py`; synthetic tests are
`tests/test_stage13_kelmarsh_zip_inventory.py`. The network entry point
requires `--execute-approved-read` and has **not** been run. Its exact code
SHA-256 in this proposal is
`0e3e631bf8010d8d29dd3847cdc6057ee842ed9723ebfc95dae42bec76dc112c`;
the canonical Git blob **and raw worktree bytes** must both match that value
after pre-read QA and immediately before any authorized execution. A Windows
CRLF checkout mismatch stops the run until the worktree is restored to the
canonical LF bytes. No change to the historical Stage 06 hashes is needed.

## Why this order is cheap

The directory may identify per-turbine member names and sizes using at most
0.134% of the listed archive bytes. This can reject an unsuitable archive
without obtaining the remaining 97.8 MB. It **cannot** establish 27 genuine
concurrent channels, finite/missingness coverage, paired 11/26/>26 views,
independent farms or a clean split. If the inventory succeeds, propose a
separate deterministic, audit-only **2016** member/schema and finite-count
pilot. Exclude the entire 2016 year from any future formal role before a
member or measurement read; obtain separate PI source/use, role and split
decisions before admission. No other annual archive is silently substituted.

## Two separate PI gates before execution

1. **Staffing:** permit one additional read-only follow-up by an existing
   independent QA reviewer for this exact request, script and synthetic tests.
   DEC-100 exhausted the earlier reserved follow-up. The reviewer must report
   `PASS` before the range request. This is a one-review expansion of the
   per-agent ceiling, not a new specialist or broader Stage 13 budget.
2. **Source-file access:** approve or hold the exact one-range, 131,072-byte
   memory-only ZIP-directory read above. A QA `PASS` does not itself grant
   access; the PI must decide this gate separately. A failed request gets no
   automatic retry, member read or archive download.

Electricity and all test signals/scores remain sealed. PhysioNet stays on
source/use `HOLD`; H-04 is `not tested`; no protocol/budget freeze, Stage 14
entry, model execution or public release follows from this inventory.
