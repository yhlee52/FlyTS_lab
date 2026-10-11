# Proposed independent QA of DEC-104 ZIP inventory result

Status: **one existing-reviewer read-only follow-up PI `GO` (DEC-105),
completed with [bounded `PASS`](KELMARSH_ZIP_INVENTORY_RESULT_QA.md)**.
DEC-103's one pre-read follow-up is consumed by the
[PASS review](KELMARSH_ZIP_INVENTORY_PREREAD_QA.md). This request does not
increase the specialist count or two-agent parallel ceiling.

The exact review is one bounded check of
`KELMARSH_ZIP_INVENTORY_RESULT.md`, DEC-104, the approved request, the
executed `tools/stage13_kelmarsh_zip_inventory.py` code/hash, and the seven
synthetic tests. The reviewer should check the two reported ranges and 1,198
application bytes, directory count and six data/six status member summary,
hash/CI provenance, absence of unsupported 27-channel, source-admission or
split claims, and the Stage 13/14/test/release boundaries. The reviewer may
rerun local synthetic tests and governance/notebook validation.

**No source replay:** DEC-104's exact two-request access is exhausted. QA
must not contact Zenodo, read an archive/member or inspect signal values,
arrays, model scores, Electricity or test material. Response bytes, span
SHA-256 values and member listing remain Director-reported. QA should give
`PASS`/`CONDITIONAL PASS`/`FAIL` for report consistency and claim limits,
explicitly stating that it did not independently verify source responses.
The reviewer edits no tracked files and stops after this one review.

This staffing decision alone grants no member/header/signal access,
source/use, audit-only exclusion, role or split, protocol/budget freeze,
Stage 14 entry or public release. A later pilot needs its own exact packet,
PI decisions and independent pre-read QA.
