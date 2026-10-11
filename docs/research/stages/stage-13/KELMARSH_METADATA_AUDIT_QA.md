# Kelmarsh v4 metadata audit: independent QA

Verdict: **CONDITIONAL PASS for the DEC-096 access boundary; metadata
eligibility and Stage 13 freeze HOLD**. Reviewed 2026-10-11 by an independent
QA reviewer. This is not source/use admission, role or split approval.

## Scope and checks

The reviewer inspected DEC-096, the exact access request, the executed
`tools/stage13_kelmarsh_metadata_audit.py`, the synthetic tests and the
Director's audit record. The script fixes the two approved Zenodo filenames,
published sizes and MD5s, rejects redirects and unexpected final URLs,
requires HTTP 200, the declared lengths and identity encoding, caps each
read and the combined application bytes at 3,957, and verifies MD5 before
CSV parsing. It contains no source-file write path. The synthetic
`unittest` suite passed **4/4** without contacting Zenodo.

The reviewer did **not** replay source access. The reported 3,150 + 807
received bytes, publisher MD5 matches, local SHA-256 values, response
behavior and lack of external capture are Director-reported observations.
The tests do not cover truncated bodies or MD5 failure.

## Conditional findings

- A synthetic reproduction showed that the extractor selected the 60
  `Greenbyte Signal ID` values but omitted both title columns, and selected
  no values for the static `Identity`/`Title` fields. Consequently it cannot
  classify native signals or list the six turbine IDs as planned.
- The execution emitted 60 signal-ID values to a tool transcript. Whether
  those values count as permitted "field-name" summaries under DEC-096 is
  ambiguous. They were not committed or saved as source content, and no
  measured signal values were emitted. Treat this as a possible output-scope
  deviation and do not reuse the list for eligibility decisions.
- The approved byte cap is exhausted. Correcting the omissions requires a
  new, exact PI access decision and independent review of the corrected
  extraction path before another source read.

Mapping-row and static-row counts cannot establish 27 simultaneous usable
channels, independent farms, or a leakage-safe held-out split. Kelmarsh
source/use, role, split and H-01 count remain `HOLD`; H-04 remains
`not tested`. Electricity/test stay sealed. Stage 09 history and DEC-070
public-release `STOP` are unchanged.
