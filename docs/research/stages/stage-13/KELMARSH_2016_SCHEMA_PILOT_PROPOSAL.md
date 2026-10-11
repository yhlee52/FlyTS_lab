# Proposed lowest-byte Kelmarsh 2016 schema pilot

Status: **proposal only; no access, audit-only exclusion or staffing approval**.
Stage 13 remains `HOLD`. This packet follows the bounded DEC-104 ZIP directory
inventory and its [independent report QA](KELMARSH_ZIP_INVENTORY_RESULT_QA.md).

## Fixed question and source

Does the first, preselected `Turbine_Data_Kelmarsh_1_2016-01-03_-_2017-01-01_228.csv`
member have a parseable SCADA CSV header with enough candidate columns to
justify a later finite-channel availability audit? The official Cubico
Kelmarsh v4 owner record is CC BY 4.0; that public-data condition supports a
request for **audit-only** access, not automatic formal source admission.
The six directory-listed turbines share one farm. A member name and header
cannot establish 27 simultaneous usable channels, independent farms, paired
11/26/>26 views, time coverage or a valid formal split.

## Proposed two-stage PI gate

1. **Source/use and exclusion:** Decide whether Kelmarsh v4 may be read solely
   for this bounded schema audit, with the entire **2016 year of all six
   turbines excluded** from every future pretrain, development, final and
   test role. This is an audit-only exclusion, not admission or a formal
   train/validation/test split. If this condition is unacceptable, retain
   `HOLD` and do not read a member.
2. **Exact access and QA staffing:** If the first decision is `GO`, consider
   one HTTP Range of **bytes 0–8191** from the same 97,915,553-byte official
   `Kelmarsh_SCADA_2016_3082.zip` URL used in DEC-104. Maximum application
   source bytes: **8,192**, once, with no retry, redirect or full-file
   fallback. Authorize one existing reviewer pre-read code/fixture QA and
   one bounded result QA separately; the current follow-up budget is exhausted.
   A final script, synthetic tests, exact script hash and independent pre-read
   `PASS` must exist before access. This proposal alone is not executable.

The script must require HTTP 206, exact URL, `Content-Range` including the
published total, `Content-Length`, identity encoding and an exact 8,192-byte
body. It must verify a ZIP local-header signature at offset zero, reject
encryption/unsupported compression, and require the exact preselected member
name. If offset zero contains another member or the header is malformed,
stop without trying another range or choosing another member.

Only after those checks may it inflate a bounded prefix of that member to
find its first CSV line. This **does read compressed measurement payload** and
may temporarily inflate part of the first data row; neither raw nor inflated
bytes may be stored. Bound decompressed output and stop at the first line;
emit only the member identity, parser/byte counts, schema column count and
bounded header names/hashes. Do not inspect or report measurement values,
timestamps, score, missingness or target labels. If the line is incomplete
within the one range, record inconclusive `HOLD`, with no automatic repeat.
The whole-archive MD5 and member CRC remain unverified.

If the header has too few plausible measurement columns or the first member
does not match, reject this exact low-byte route and seek a new PI decision
before any alternative. If it is promising, a later, separately approved
finite/missingness audit must establish actual concurrent usable channels and
the same-record paired views. Formal source/use, role and split admission
remain separate PI gates. The 2016 audit year never becomes formal evidence.

No other archive, turbine, member, source signal, Electricity/test item, model
training/evaluation, protocol/budget freeze or Stage 14 entry is authorized.
H-01 count and H-04 remain untested; Q2/Q3 unavailable; DEC-070 release
`STOP` persists.
