# Proposed minimum-byte Kelmarsh ZIP inventory gate

Status: **revised two-Range access PI `GO` (DEC-104), independent pre-read QA
`PASS`; one execution completed and its access cap exhausted**. See the
[Director-reported result](KELMARSH_ZIP_INVENTORY_RESULT.md). The original
one-Range DEC-103 access is withheld after QA found it could include compressed
member payload. DEC-103's single reviewer follow-up completed with
[PASS](KELMARSH_ZIP_INVENTORY_PREREAD_QA.md) on the correction. Route A
(DEC-102) preserves the Stage 11 H-01–H-03 contract;
source/use, role and split remain unapproved. Stage 13 freeze remains `HOLD`.

## Exact first unit

The [Cubico Kelmarsh v4 owner record](https://zenodo.org/records/16807551)
lists its smallest annual SCADA ZIP as `Kelmarsh_SCADA_2016_3082.zip`. The
[official record metadata](https://zenodo.org/api/records/16807551) reports
exactly **97,915,553 bytes**, publisher MD5
`ca8efbb6dbcfae3516583937eb5b5402`, and this exact content URL:

`https://zenodo.org/api/records/16807551/files/Kelmarsh_SCADA_2016_3082.zip/content`

The revised first source read is exactly **two HTTP GET Ranges**, with a
combined application-read cap of **131,072 bytes** and no retry or full-file
fallback:

1. Read only the last **22 bytes**, `bytes=97915531-97915552`, the location of
   a standard ZIP end-of-central-directory (EOCD) record without a comment.
   Require zero comment length, single disk, at most 128 entries, no ZIP64,
   central-directory size between 1 and 131,050 bytes, and an offset placing
   the directory immediately before those final 22 bytes. If any check fails,
   stop after this first request. On an invalid ZIP those 22 bytes are opaque
   trailer bytes, never parsed as a member.
2. Only after the EOCD checks, read the **exact directory span** given by its
   offset and size. For a valid ZIP, this excludes local headers and
   compressed members. A malformed or spoofed EOCD could point this bounded
   second request at opaque bytes, including compressed member bytes. The
   parser rejects a non-directory signature after receipt; it never decodes
   or emits those bytes. This is **not an absolute zero-payload-byte guarantee**
   for a malformed source; DEC-104 explicitly covers this bounded
   opaque-byte possibility.

Both responses must be HTTP 206 from the exact URL, with exact
`Content-Range` start/end/total, exact `Content-Length`, and identity encoding
before body reads. HTTP 200, redirect, size mismatch, short response,
unsupported layout or malformed directory stops at `HOLD`. A failed first
request produces no second request.

Parse only the ZIP end and central directory. Emit at most 128 member names,
compressed/uncompressed byte counts, compression methods, encryption flags,
CRC-32 values, both range coordinates and byte counts, and the SHA-256 of each
metadata span. Do not open a member or
emit a CSV header, timestamp, measurement, event, array or score. Keep the
two spans in memory and save no source bytes. The publisher MD5 covers the
**whole archive** and cannot be verified from these spans; `Content-Range`
and span SHA-256 are bounded provenance, not source identity proof. Transport-layer
buffering beyond application reads is not measured.

The tool is `tools/stage13_kelmarsh_zip_inventory.py`; synthetic tests are
`tests/test_stage13_kelmarsh_zip_inventory.py`. The network entry point
requires `--execute-approved-read`. It had not been run when this access was
proposed; the one DEC-104 execution is reported separately. Its exact code
SHA-256 for that execution is
`781840249016735cbf2953af5ca3d33f0dd20e26003d3e99f82f4f3510b02986`;
the canonical Git blob **and raw worktree bytes** were required to match that
value immediately before the DEC-104 execution and did match, as reported in
the result. The Windows CRLF checkout check did not change the historical
Stage 06 hashes.

## Why this order is cheap

The directory may identify per-turbine member names and sizes using at most
0.134% of the listed archive bytes, and usually much less. This can reject an unsuitable archive
without obtaining the remaining 97.8 MB. It **cannot** establish 27 genuine
concurrent channels, finite/missingness coverage, paired 11/26/>26 views,
independent farms or a clean split. If the inventory succeeds, propose a
separate deterministic, audit-only **2016** member/schema and finite-count
pilot. Exclude the entire 2016 year from any future formal role before a
member or measurement read; obtain separate PI source/use, role and split
decisions before admission. No other annual archive is silently substituted.

## Two separate PI gates before execution

1. **Staffing — GO, DEC-103:** one additional read-only follow-up by an existing
   independent QA reviewer for this exact request, script and synthetic tests.
   DEC-100 exhausted the earlier reserved follow-up. The reviewer must report
   `PASS` on this revised code and request before any range. This is a one-review expansion of the
   per-agent ceiling, not a new specialist or broader Stage 13 budget.
2. **Source-file access — GO, DEC-104:** the exact two-range,
   at-most-131,072-byte memory-only ZIP-directory read above. DEC-103's
   one-range approval is not used because it does not ensure the stated
   no-member-payload boundary. The separate DEC-104 decision grants the
   revised bounded access, conditional on the final code/CI preflight.
   Failure gets no automatic retry, member read or archive download.

Electricity and all test signals/scores remain sealed. PhysioNet stays on
source/use `HOLD`; H-04 is `not tested`; no protocol/budget freeze, Stage 14
entry, model execution or public release follows from this inventory.
