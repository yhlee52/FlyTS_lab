# Kelmarsh 2016 bounded first-line pilot result

Status: **DEC-107's one exact Range completed; Director-reported result;
independent result QA pending; Stage 13 freeze HOLD**. Executed 2026-10-11
from Draft PR #35 head `cde9698` after independent pre-read QA `PASS`, both
head CI `pytest` jobs `PASS` (4m06s and 2m23s), local 18 synthetic checks
`PASS`, and byte-exact preflight. The Git blob and raw worktree SHA-256 of
`tools/stage13_kelmarsh_schema_pilot.py` both matched
`28dad91664e48a2a8293460dc993c54efa1950a13da7411a8f8eb2022f487c14`
immediately before execution.

The script reported one HTTP Range `bytes=0-8191` from the official Cubico
Kelmarsh v4 `Kelmarsh_SCADA_2016_3082.zip` content URL. Its inherited client
accepted HTTP 206 only with exact URL, `Content-Range`, `Content-Length` and
identity encoding. It read **8,192 application bytes**, kept them in memory,
and reported prefix SHA-256
`51c4aef9689d087a48bd8f9f2572683054f42e9f0bdbf8a1a567f61c1ee7cfc4`.
The ZIP local header at offset zero identified the preselected
`Turbine_Data_Kelmarsh_1_2016-01-03_-_2017-01-01_228.csv` member. The
parser consumed 224 compressed bytes and transiently inflated 138 bytes to
reach the first newline. It emitted no field or measurement values. The
first-line SHA-256 was
`c49b8ac7c54406704a102f72d36dd49c0d0565463d584b6efb096b93b021e7f4`.

**Observed parser result:** the first line contained **one CSV field under
the tool's comma delimiter**. Header identity is `unverified`. That one
field may be a metadata line, a header using another delimiter, or a data
line. It is **not** evidence that this turbine has one channel or lacks 27
usable channels. No raw first-line text was emitted or retained. The whole
archive MD5 and member CRC remain unverified. The HTTP response, hashes and
no-retry report are Director-reported; result QA must not replay the source.

DEC-107's one source read is exhausted. There is no authorized automatic
reparse from saved bytes, second Range, alternative member or year, admission,
role/split or protocol change. All six turbines' 2016 data remains audit-only
and excluded from every future formal role under DEC-106. A later delimiter/
schema investigation requires a new exact PI access and QA packet; this
pilot cannot establish simultaneous finite channel coverage, paired 11/26/>26
views, time coverage or independent-domain inference. H-01 count remains
untested. Stage 13 stays `HOLD`, H-04 `not tested`, Q2/Q3 unavailable,
Electricity/test sealed, Stage 14 `NO GO`, Stage 09 history unchanged and
DEC-070 public release `STOP` active.
