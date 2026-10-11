# Kelmarsh first-line pilot: independent result QA

Verdict: **PASS for bounded DEC-107 report consistency and claim limits**,
2026-10-11. This does not independently verify the Zenodo response or admit
the source. DEC-106's reserved result-review follow-up is exhausted.

The reviewer checked the Director's one-Range report, DEC-106/107, pre-read
QA, proposal, script and tests. The report records `bytes=0-8191`, **8,192
application bytes**, the fixed turbine-1 member, and **one first-line field
under the comma parser**. It explicitly leaves the line's header identity,
delimiter and channel count unverified. The script emits only a field count
and hashes, no raw first-line values. Local synthetic tests passed **11/11**
pilot and **7/7** inherited inventory checks; research governance, notebook
and diff checks passed. The Git blob and worktree script SHA-256 both match
`28dad91664e48a2a8293460dc993c54efa1950a13da7411a8f8eb2022f487c14`.
Both supplied GitHub `pytest` job IDs show success. The first job's exact-head
association was Director-reported; the second was independently associated
with execution head `cde9698`. A stale proposal sentence was corrected during
review.

**Evidence limit:** The reviewer did not replay Zenodo. The network response,
prefix SHA-256, first-line SHA-256, member identity and no-retry account remain
Director-reported. Whole-archive MD5 and member CRC are unverified. A first
line with one comma-delimited field is not evidence of one channel or failure
to meet 27 channels. No simultaneous finite coverage, paired count view,
time range or formal split can be inferred.

DEC-107 access and both DEC-106 QA follow-ups are exhausted. All six turbines'
2016 data is audit-only and excluded from future formal roles. Source/use
admission, role/split, protocol/budget freeze and Stage 14 remain closed;
Stage 13 is `HOLD`, H-04 `not tested`, Electricity/test sealed and DEC-070
public release `STOP` active.
