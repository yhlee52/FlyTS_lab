# Kelmarsh 2016 ZIP inventory result

Status: **DEC-104's one bounded read completed; Director-reported result,
independent result QA pending; Stage 13 freeze HOLD**. Executed 2026-10-11
from Draft PR #35 after independent pre-read QA `PASS`, two GitHub `pytest`
checks `PASS`, seven synthetic tests `PASS`, and a byte-exact script preflight.
The canonical Git blob and raw worktree SHA-256 of
`tools/stage13_kelmarsh_zip_inventory.py` both matched
`781840249016735cbf2953af5ca3d33f0dd20e26003d3e99f82f4f3510b02986`
immediately before execution. The source was not stored.

## Exact bounded response

The tool issued the two approved HTTP Ranges to the official v4
`Kelmarsh_SCADA_2016_3082.zip` content URL. Both passed its HTTP 206,
exact-URL, `Content-Range`, `Content-Length` and identity-encoding checks.

| Span | Bytes | SHA-256 of received bytes |
|---|---:|---|
| EOCD `97915531-97915552` | 22 | `1aeda797fbd46b61c6c52f028409e94fb697c25dab48a4ead2252f6f3bf5a1e6` |
| Central directory `97914355-97915530` | 1,176 | `ff63c351fca38900cac758c6ca28701ba4217e1678209f67170bac85a8ef8581` |

Total application bytes read: **1,198**. No retry, redirect, full ZIP fetch,
local member read, decompression, CSV header, measurement, model output,
Electricity or test item was accessed. These are Director-reported execution
facts; QA has not independently replayed the network response. The publisher
whole-archive MD5 `ca8efbb6dbcfae3516583937eb5b5402` remains
**unverified** by this partial access.

## Directory-only inventory

The directory lists **12 members**: six `Turbine_Data` CSVs and six `Status`
CSVs, one pair each for turbine numbers 1–6 and IDs 228–233. All entries
declare ZIP deflate method 8 and no encryption. Each filename contains
`2016-01-03_-_2017-01-01`, which is a filename assertion, not verified time
coverage. The six data-member sizes in turbine order are:

| Turbine / ID | Data member compressed bytes | Data member uncompressed bytes | Status member compressed bytes |
|---|---:|---:|---:|
| 1 / 228 | 16,494,707 | 90,955,830 | 23,513 |
| 2 / 229 | 16,418,010 | 90,969,476 | 20,450 |
| 3 / 230 | 16,358,791 | 90,774,387 | 29,021 |
| 4 / 231 | 16,324,728 | 90,629,557 | 20,705 |
| 5 / 232 | 16,311,235 | 90,848,710 | 22,556 |
| 6 / 233 | 15,858,373 | 90,257,527 | 31,282 |

The directory also declares per-member CRC-32 values, but none can be
verified without full member reads. The bounded directory read supports a
deterministic next **proposal** targeting turbine 1 / ID 228 for an audit-only
2016 schema/finite-count pilot. It does **not** prove the number of CSV
columns, genuine simultaneous measurements, 27 finite channels, paired
11/26/>26 views, independent farms, source identity beyond the checked range
headers, or a leakage-free formal split. The six turbines share one farm.

DEC-104's access is exhausted. A result QA follow-up, any member or signal
read, source/use admission, audit-only exclusion, development role and formal
split each need their own applicable PI decision. The Stage 11 contract is
unchanged; H-01 count remains untested, H-04 `not tested`, Q2/Q3 unavailable,
Stage 14 `NO GO`, Stage 09 history intact and DEC-070 release `STOP` active.
