# Kelmarsh ZIP inventory pre-read QA

Verdict: **PASS for the revised two-Range code and bounded request at
`f98c5ca`; source access remains `HOLD` pending a new PI decision**.
Date: 2026-10-11. This is the one additional read-only follow-up authorized
by DEC-103; it is not source-result QA or protocol pre-freeze QA.

The reviewer found that the earlier 131,072-byte suffix could include
compressed member payload, so the Director withheld DEC-103's original
one-Range read before execution. The revised tool requests exactly the final
22 bytes first. It then checks the standard no-comment EOCD and the combined
131,072-byte cap before requesting the declared central-directory span. Both
responses require HTTP 206, the exact URL, range, length and identity
encoding. The code has no retry or full-download path and does not open,
decompress or emit a ZIP member.

The reviewer ran the seven synthetic tests, including a spoofed-offset case,
and the governance/notebook validators; all passed. `git diff --check` passed.
Stage 09 tracked files remain unchanged. The canonical Git blob and raw
worktree SHA-256 for `tools/stage13_kelmarsh_zip_inventory.py` both matched
`781840249016735cbf2953af5ca3d33f0dd20e26003d3e99f82f4f3510b02986`.

**Residual limit:** a malformed or spoofed EOCD could direct the second,
bounded request to opaque bytes that include compressed member data before
the parser rejects the non-directory signature. The [revised
request](KELMARSH_ZIP_INVENTORY_REQUEST.md) discloses this. Its new PI access
decision must explicitly cover that possibility. QA `PASS` does not grant
access. The code hash needs rechecking immediately before any approved run.

The reviewer did not contact Zenodo or inspect source bytes, measurements,
arrays, scores, Electricity or test material. Publisher size/MD5, actual ZIP
layout and concurrent-channel eligibility remain unverified. This review
grants no source/use, role/split admission, protocol/budget freeze, Stage 14
entry or public release.
