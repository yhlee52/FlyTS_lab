# Kelmarsh v4 mapping-title correction audit

Status: **DEC-097's single mapping read completed; result QA pending;
source/use, role, split, H-01 count and Stage 13 freeze HOLD**. Executed
2026-10-11 with Python 3.14.5 after independent [pre-read QA
PASS](KELMARSH_MAPPING_PREREAD_QA.md). The executed
`tools/stage13_kelmarsh_mapping_correction.py` SHA-256 was checked
immediately before the read and matched
`a3708de74ad9f33dd1fb791bea1987edbde1e37bbf0d1b96656eaec302341426`.

The script made **one request** to the exact approved
`Kelmarsh_WT_dataSignalMapping.csv` endpoint of the official [Cubico
Kelmarsh v4 record](https://zenodo.org/records/16807551). It accepted HTTP
200, the exact final URL, identity encoding and declared length, read
**3,150 application bytes in memory**, and matched publisher MD5
`ca8fe399ab15ae7111d3214c632efd36`. The source SHA-256 was
`2dad8552ba4d45d59b9a778c68025b8c3614179d48dfb938c3af07c90ebd06af`,
the same value reported for that file under DEC-096. There was no retry.
No source CSV, signal, array, model output or checkpoint was saved to disk.

The output contained the schema field names, **60 complete title pairs**
from `Greenbyte Title` and `Manufacturer Title`, tentative category counts
and hashes. It contained no `Greenbyte Signal ID` values. The title pairs
were emitted only to the execution tool transcript, not committed to Git.
The schema still has four fields and 60 rows. The scripted title-keyword
flags were: status/alarm **0**, setpoint/limit **1**, aggregate/derived
**0**, repeated title **4**, and not flagged **55**. Categories may overlap.
The repeated-title flag counts a title repeated across the two naming
columns, including within the *same mapping row*; it does **not** establish
four duplicated channels. Zero keyword flags does not establish absence of
status, derived or unusable signals.

These names show that the mapping enumerates diverse electrical, mechanical
and environmental quantities, but neither 60 names nor 60 rows prove 27
genuinely concurrent usable channels on each turbine. The official record
warns that signal availability varies by period. No SCADA ZIP, annual
header, measured value, missingness, paired 11/26/>26 views, independent
farm, time split, test/Electricity item or model score was accessed. The
six static rows from DEC-096 are one shared farm, not six independent
farms. No source/use admission, role, split, protocol or compute decision
follows from this read. H-04 remains `not tested`, Q2/Q3 unavailable,
Stage 09 history intact and DEC-070 public release `STOP` in force.

The 3,150-byte DEC-097 cap is exhausted. Any further source read requires
a new exact PI decision. Independent result QA has not replayed the source;
the received bytes, hash and parsed output above are Director-reported
execution evidence pending that review.
