# Proposed lowest-byte Kelmarsh 2016 schema pilot

Status: **DEC-106 approved audit-only 2016 exclusion and tool/QA preparation;
independent [pre-read QA PASS](KELMARSH_2016_SCHEMA_PILOT_PREREAD_QA.md),
source-file access pending**. Stage 13
remains `HOLD`. This packet follows the bounded DEC-104 ZIP directory
inventory and its [independent report QA](KELMARSH_ZIP_INVENTORY_RESULT_QA.md).

## Fixed question and source

Does the first, preselected `Turbine_Data_Kelmarsh_1_2016-01-03_-_2017-01-01_228.csv`
member have a parseable **first CSV line** with enough fields to justify a
later verified-schema and finite-channel availability audit? Header identity
cannot be established from that line alone. The official Cubico
Kelmarsh v4 owner record is CC BY 4.0; that public-data condition supports a
request for **audit-only** access, not automatic formal source admission.
The six directory-listed turbines share one farm. A member name and header
cannot establish 27 simultaneous usable channels, independent farms, paired
11/26/>26 views, time coverage or a valid formal split.

## Proposed two-stage PI gate

1. **Audit-only exclusion and preparation — PI GO, DEC-106:** Kelmarsh v4 may
   be considered for this bounded schema audit, with the entire **2016 year
   of all six turbines excluded** from every future pretrain, development,
   final and test role. This is not formal source/use admission or a formal
   train/validation/test split. No member read follows from this decision.
2. **Exact access pending; QA staffing GO, DEC-106:** Consider
   one HTTP Range of **bytes 0–8191** from the same 97,915,553-byte official
   `Kelmarsh_SCADA_2016_3082.zip` URL used in DEC-104. Maximum application
   source bytes: **8,192**, once, with no retry, redirect or full-file
   fallback. DEC-106's existing-reviewer pre-read code/fixture QA returned
   `PASS`; one later result QA follow-up remains reserved.
   A final script, synthetic tests, exact script hash and independent pre-read
   `PASS` and a separate PI access `GO` must exist before execution.

The prepared tool is `tools/stage13_kelmarsh_schema_pilot.py`; its current raw
worktree SHA-256 is
`28dad91664e48a2a8293460dc993c54efa1950a13da7411a8f8eb2022f487c14`.
The canonical Git blob and raw worktree bytes must match this hash after
independent pre-read QA and immediately before any separately approved read.
The new synthetic tests are `tests/test_stage13_kelmarsh_schema_pilot.py`.
This fingerprint and proposal do not authorize execution.

The script must require HTTP 206, exact URL, `Content-Range` including the
published total, `Content-Length`, identity encoding and an exact 8,192-byte
body. It must verify a ZIP local-header signature at offset zero, reject
encryption/unsupported compression, and require the exact preselected member
name. If offset zero contains another member or the header is malformed,
stop without trying another range or choosing another member.

Only after those checks may it inflate a bounded prefix of that member to
find its first CSV line. This **does read compressed measurement payload** and
may temporarily inflate part of the first data row; neither raw nor inflated
bytes may be stored. Cap total decompressed output at **65,536 bytes**, the
first line including newline at **8,192 bytes**, and parsed fields at **128
fields of at most 256 characters each**; stop at the first line. Emit only
member identity, parser/byte counts, the first-line field count and first-line
SHA-256. **Do not emit field values or call them confirmed header names.**
Do not inspect or report measurement values,
timestamps, score, missingness or target labels. If the line is incomplete
within the one range, record inconclusive `HOLD`, with no automatic repeat.
The whole-archive MD5 and member CRC remain unverified.

If the first line has too few fields or the first member does not match,
reject this exact low-byte route and seek a new PI decision before any
alternative. If it is promising, a later, separately approved schema and
finite/missingness audit must establish actual concurrent usable channels and
the same-record paired views. Formal source/use, role and split admission
remain separate PI gates. The 2016 audit year never becomes formal evidence.

No other archive, turbine, member, source signal, Electricity/test item, model
training/evaluation, protocol/budget freeze or Stage 14 entry is authorized.
H-01 count and H-04 remain untested; Q2/Q3 unavailable; DEC-070 release
`STOP` persists.
