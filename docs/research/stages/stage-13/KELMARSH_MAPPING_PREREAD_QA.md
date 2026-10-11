# Kelmarsh mapping correction: independent pre-read QA

Verdict: **PASS for the one DEC-097 mapping-only read**, 2026-10-11. This
does not establish source eligibility or approve a second request.

The independent reviewer inspected DEC-097, the exact correction request,
`tools/stage13_kelmarsh_mapping_correction.py`, its shared bounded reader
and both synthetic test files. The corrected script SHA-256 reviewed for
execution is `a3708de74ad9f33dd1fb791bea1987edbde1e37bbf0d1b96656eaec302341426`.
The reviewer made no Zenodo or other source read.

The code calls the shared reader once for the one named 3,150-byte file.
That reader requires the exact URL, HTTP 200, declared length, identity
encoding, the application-byte cap and publisher MD5, and disables
redirects. Neither script has a source-file write path. The output contains
only metadata schema names, at most 60 pairs of `Greenbyte Title` and
`Manufacturer Title` values, tentative category counts and the evidence
SHA-256; it does not re-emit or reuse Signal ID values. Exactly 60 complete
mapping rows are required. Failures return `HOLD`.

The reviewer ran both synthetic suites: **8/8 tests passed**. Actual
response bytes, publisher MD5, schema and titles were unverified during QA.
The earlier DEC-096 output-scope ambiguity remains on record. Title-keyword
flags cannot establish 27 usable concurrent channels, independent turbines,
source admission or a split. Any failed request or changed script requires
`HOLD` under DEC-097.
