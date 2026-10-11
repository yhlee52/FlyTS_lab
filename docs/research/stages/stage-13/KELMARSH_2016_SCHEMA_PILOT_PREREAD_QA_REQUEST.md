# Kelmarsh 2016 schema pilot: independent pre-read QA request

Status: **DEC-106 grants one existing-reviewer read-only follow-up; review
pending.** No member or signal access is approved. The exact proposal is
[here](KELMARSH_2016_SCHEMA_PILOT_PROPOSAL.md).

Review the fixed turbine-1 first-member choice and audit-only 2016 exclusion;
the one `bytes=0-8191` request and HTTP fail-closed checks inherited from
`stage13_kelmarsh_zip_inventory.py`; ZIP local-header and deflate validation;
8,192 source-byte, 8,192 header-line, 65,536 decompressed-output and bounded
column-name limits; absence of extra Range/retry/fallback/source storage; and
synthetic malformed-source checks. Verify the script's canonical Git blob and
raw worktree SHA-256 against
`48c71111f07553005ed9bcd5ef7e098b47ceb879e09f116a4d51454c45687b25`.
Run local synthetic tests, governance/notebook validators and diff checks.

Inspect code and tracked documents only. **Do not run the executable flag,
contact Zenodo, open an archive/member, inspect any signal/test/Electricity
material, or edit tracked files.** Give PASS/CONDITIONAL PASS/FAIL and note
whether any data-access risk remains. A pre-read `PASS` alone does not grant
the separate PI source-file access decision. The second DEC-106 reviewer
follow-up is reserved solely for an eventual result review if access is later
approved and executed.
