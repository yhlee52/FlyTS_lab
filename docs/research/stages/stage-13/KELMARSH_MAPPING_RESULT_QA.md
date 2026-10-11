# Kelmarsh mapping correction: independent result QA

Verdict: **PASS for the bounded DEC-098 result review**, 2026-10-11.
This is a provenance-and-claim review, **not** independent verification of
the Zenodo response or source admission.

The independent reviewer inspected DEC-097/098, the correction script and
synthetic tests, the pre-read QA, the Director's execution audit and the
earlier DEC-096 audit. The current correction script SHA-256 is
`a3708de74ad9f33dd1fb791bea1987edbde1e37bbf0d1b96656eaec302341426`,
matching the pre-read and execution records. The focused synthetic suite
passed **4/4**. The script outputs title pairs and does not emit Signal ID
column values.

The audit reports one 3,150-byte read, the approved publisher MD5 and
source SHA-256 `2dad8552ba4d45d59b9a778c68025b8c3614179d48dfb938c3af07c90ebd06af`,
consistent with the earlier DEC-096 report. These are **Director-reported
access facts**: DEC-098 prohibited a replay. The reviewer could not
independently verify response bytes, MD5, SHA-256, the 60 actual title
pairs, category totals or absence of external capture. Matching hashes in
two Director reports are not two independent measurements.

No defect was found in the packet's provenance consistency or claim
limits. The repeated-title flag can arise within one row across the two
title columns; four flags are not four duplicate channels. Zero keyword
flags is not proof that all entries are usable. Sixty mapping rows cannot
establish 27 concurrent channels per turbine, period missingness or
independent-farm evidence. Both approved Kelmarsh access caps are
exhausted. Source/use, role, split, H-01 count, Stage 13 freeze and any
further source access remain `HOLD` or separately gated. H-04 remains
`not tested`, Electricity/test sealed, Stage 09 history unchanged and
DEC-070 public-release `STOP` in force.
