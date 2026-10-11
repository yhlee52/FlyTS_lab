# Kelmarsh ZIP inventory: independent result QA

Verdict: **PASS for the bounded DEC-105 report-consistency and claim review**,
2026-10-11. This is not an independent replay of the Zenodo response, source
admission, or Stage 13 pre-freeze QA.

The reviewer checked the DEC-104/105 scope, access request and pre-read QA,
Director's [result](KELMARSH_ZIP_INVENTORY_RESULT.md), inventory script and
seven synthetic tests. The reported spans are contiguous and correctly sized:
22 EOCD bytes plus 1,176 central-directory bytes = **1,198 application bytes**.
The reported six turbine-data and six status compressed sizes fit the listed
97,915,553-byte archive with 984 bytes before the directory for ZIP overhead.
The script's Git blob and raw worktree SHA-256 both match
`781840249016735cbf2953af5ca3d33f0dd20e26003d3e99f82f4f3510b02986`.
Seven local synthetic tests, research governance, notebook and diff checks
passed. GitHub's `pytest` jobs passed on pre-execution PR #35 commits
`f98c5ca` (run `38145905580`) and `d58d3ee` (run `38146072639`). Stage 09
tracked files remain unchanged. A stale pre-execution sentence in the access
request was corrected during this review.

**Evidence limit:** The reviewer did not contact Zenodo. Both HTTP responses,
their span hashes, the 12-member listing and the reported absence of retries
remain Director-reported, not independently observed. The whole-archive MD5
and member CRCs remain unverified. Directory names and sizes do not prove
CSV columns, 27 concurrent finite channels, time coverage or a formal split.

DEC-105 is exhausted. There is no further source access, source/use admission,
role or split decision, protocol or budget freeze, or Stage 14 entry. Stage 13
remains `HOLD`, H-04 `not tested`, Electricity/test sealed and DEC-070 public
release `STOP` active.
