# Kelmarsh 2016 first-line pilot: independent pre-read QA

Verdict: **PASS for code and bounded proposal on Draft PR #35 head
`a0821e4`**, 2026-10-11. This is not source access approval or validation of
Kelmarsh content. DEC-106's one pre-read reviewer follow-up is exhausted.

The reviewer reproduced two defects in the earlier draft: a headerless data
row could be emitted as header names, and an 8,193-byte physical line could
pass the stated 8,192-byte cap. Both were fixed before this verdict. The
revised tool emits only the first-line field count and SHA-256, labels header
identity `unverified`, and counts the newline in the line cap. It fixes the
first member, uses one exact `bytes=0-8191` Range through inherited fail-closed
HTTP checks, and has no retry or source-byte storage path.

Local synthetic checks passed **11/11** for this pilot and **7/7** inherited
inventory tests. Research governance, notebook and diff checks passed. The
canonical Git blob and raw worktree SHA-256 of
`tools/stage13_kelmarsh_schema_pilot.py` both matched
`28dad91664e48a2a8293460dc993c54efa1950a13da7411a8f8eb2022f487c14`
with LF bytes. Recheck both immediately before any separately approved read.

The reviewer made **no Zenodo request**. A first-line count/hash could still
come from a headerless measurement row, although no raw fields are emitted.
It cannot establish a CSV header, 27 concurrent finite channels, temporal
coverage or split eligibility. The PI must decide the exact source-file
access with that caveat. All Kelmarsh 2016 data from six turbines remains
audit-only and excluded from future formal roles. The second DEC-106 reviewer
follow-up is reserved solely for a result review after an authorized read.

Stage 13 remains `HOLD`; no member access, source admission, protocol/budget
freeze or Stage 14 entry follows. Electricity/test stay sealed and DEC-070
public release `STOP` remains active.
