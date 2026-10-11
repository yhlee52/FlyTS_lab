# PhysioNet signal retry request: independent document/code QA

Status: **CONDITIONAL PASS** for a PI transfer decision, 2026-10-11.
Two independent read-only reviewers inspected the request, first-attempt
ledger, gate records, audit code and synthetic tests. Neither reviewer made
a network request, opened source data or edited tracked files. This is not
source-quality, member-byte or formal protocol QA.

The first reviewer found that the initial code could not detect a trailing
undeclared byte without reading beyond the approved cap, and that progress
logs lacked a cumulative EDF total. The Director corrected the request's
claim, added cumulative logging, and added synthetic checks for both.
The second reviewer found that the one-retry marker depended on the process
working directory and that a stalled connection could occur before the
active path was logged. The Director anchored report/marker paths to the
script's workspace and moved the path/total log before HTTP open. Six
stdlib synthetic tests then passed, including a failing opener and exclusive
marker creation.

The reviewers' conditional findings were corrected by the Director **after**
their reviews; no later independent `PASS` is claimed. The code still has
not been exercised against an EDF on the retry path. The first attempt's EDF
byte total is unknown. An approved retry must retain the same six paths,
one-attempt marker, hard per-file caps, publisher digest checks and failure
ledger. A further failure, missing digest or schema mismatch means `HOLD`,
with no third attempt or subject substitution. Source/use admission, formal
role/split, H-01 and protocol/compute remain separate PI gates.
