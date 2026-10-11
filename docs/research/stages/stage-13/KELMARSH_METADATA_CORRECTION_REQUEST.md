# Proposed one-file Kelmarsh metadata correction gate

Status: **proposal only; no repeat access authorized**. DEC-096's 3,957-byte
application-read cap was exhausted by one read of each approved CSV. The
independent [audit QA](KELMARSH_METADATA_AUDIT_QA.md) returned `CONDITIONAL
PASS` for the access boundary and kept eligibility `HOLD` because the
extractor omitted title and turbine-ID values. Its output included 60
`Greenbyte Signal ID` values whose inclusion in the approved "field-name"
summary is ambiguous. Those values will not be reused for admission.

## Narrow purpose and requested scope

The proposed correction is **one additional read of only** the official
Cubico Kelmarsh v4 `Kelmarsh_WT_dataSignalMapping.csv` at the
[record](https://zenodo.org/records/16807551), published size **3,150
bytes**, MD5 `ca8fe399ab15ae7111d3214c632efd36`. A new script would cap
application bytes at 3,150, make one request with no retry, require the
exact URL, HTTP 200, size, identity encoding and publisher MD5 before
parsing, and keep the file in memory only. It would emit the exact values
of the two metadata **title** columns (`Greenbyte Title`, `Manufacturer
Title`), at most 60 pairs, plus schema and category counts and a SHA-256
evidence hash. This explicitly authorizes title values as output if the PI
chooses `GO`; it does not authorize the signal-ID values again. The exact
output contract and synthetic tests need independent QA **before** the
read. The historical DEC-096 script and its hash will remain unchanged.

The proposal does not include the 807-byte static file. Its six distinct
`Identity` rows remain a bounded metadata count, while exact turbine-ID
listing stays unverified. Title categories would identify possible status,
setpoint, duplicate aggregate and derived mapping rows; labels alone would
**not** prove 27 simultaneously usable per-turbine channels. Any SCADA
header/member or measurement access, source/use admission, role and split
requires a later separate packet and PI decision.

No source content or arrays are saved, and no model, test/Electricity
signal or score, training, evaluation, checkpoint or final opening is in
scope. H-01 count and Stage 13 freeze remain `HOLD`; H-04 is `not tested`,
Stage 09 history and DEC-070 release `STOP` remain unchanged.

## Separate PI decisions needed

1. Decide whether to authorize the **new 3,150-byte mapping-only read**
   and its explicitly named title-value output, or leave this source at
   `HOLD`. DEC-096 does not authorize a second read.
2. The Stage 13 specialist follow-up ceiling has been reached for the
   independent reviewer used for DEC-096. Before pre-read QA, approve one
   additional bounded review of the corrected script, synthetic tests and
   output contract, with the Charter's two-concurrent-specialist ceiling
   unchanged. This is a QA budget decision, not data access or admission.

Both decisions and pre-read QA are required before another source request.
