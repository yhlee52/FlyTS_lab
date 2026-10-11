# Six-EDF-header pilot: independent documentation and method QA

Date: 2026-10-11. Verdict: **PASS for documentation and method review only**.
No EDF bytes were re-fetched, so this is not an independent replication of
HTTP responses, byte contents, parsing or the recorded label digest. It is
not source admission, H-01 endpoint verification or protocol pre-freeze QA.

The independent reviewer checked the [pilot record](PHYSIONET_HEADER_PILOT.md),
the [PI-approved request](PHYSIONET_HEADER_PILOT_REQUEST.md), DEC-085, Charter,
sidecar inventory and research notebook. The six paths were fixed in advance.
The stated safeguards agree with the request: official host, HTTP 206, exact
`Content-Range` and length, first 256 bytes followed only by the remaining
declared header bytes, and a 32 KiB per-file ceiling. The reviewer checked:

- `256 × (1 + 65) = 16,896` header bytes.
- `6 × 16,896 + 256` extra initial probe bytes `= 101,632` total; the
  largest per-file read was `17,152 < 32,768` bytes.
- For all six rows, `(HTTP total − 16,896) / header-declared data-record
  count = 20,640` bytes per record.
- The prior sidecar's 1,526 EDF paths minus six sampled headers leaves
  1,520 EDF headers unaccessed.

The reviewer found no document arithmetic or gate blocker. The reviewer did
not assert signal validity, paired target/reference, independent usable
subjects, rights clearance, safe split or model support. Source/use, role,
split, H-01 count and protocol v3 remain `HOLD`; Electricity/test, H-04 and
DEC-070 boundaries are unchanged. No tracked file was edited by QA.
