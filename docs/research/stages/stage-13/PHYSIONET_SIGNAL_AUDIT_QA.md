# PhysioNet six-file audit: independent source-result QA

Verdict: **PASS within the bounded audit-result and admission-readiness scope**
on 2026-10-11, at Draft PR #28 head `d2f4cd6`. This was the first of the two
extra focused follow-ups authorized for one existing independent QA reviewer
by DEC-090. No source admission, role, split or protocol freeze is implied.

The reviewer read the ignored aggregate-only JSON, tracked audit and admission
packets, DEC-087–090, the script and its synthetic tests. The aggregate's
SHA-256 matches the recorded
`9680a249e739250e9d18f725f2b7c44f17156014ec7be83a1b53c566e71bc309`.
Its six paths match the exact approved set. Each size reconciles as
`16,896 + 20,640 × one-second records`; totals reconcile to 11,515,296
completed-retry application-read EDF bytes, 553 records, 5,662,720 finite EEG
digital values and 74,481 exact digital zeros. Each 11/26/64-channel prefix
count matches its run's time coordinates. The first attempt's received bytes
remain unknown; 23,030,592 bytes is the two-attempt EDF application-read
upper bound, not a measured total.

The reviewer confirmed the S001/S055/S109 audit-only exclusion, unassigned
status of the other 106 listed subjects, ODC-By attribution and individual-
content rights caveat, separate source/role/split gates, H-01 `HOLD`, H-04
`not tested`, unavailable Q2/Q3, Electricity/test seal, Stage 09 `HOLD`/final
QA `FAIL`, and DEC-070 release `STOP`. The recorded execution-script SHA
matches its Git bytes. The Stage 09 tracked files and PR worktree are clean.

**Verification limit:** QA did not reopen EDFs, the publisher checksum
sidecar, retry marker, network logs or raw signals. Publisher digest matches
and the progress log are recorded execution claims whose consistency was
checked against the aggregate and script. These mechanical findings do not
establish physiological quality, independent held-out evidence or rights
clearance. Future access controls and manifests must enforce the three
audit-only subject exclusions. The second DEC-090 QA follow-up remains
reserved for an exact pre-freeze packet if one becomes valid.
