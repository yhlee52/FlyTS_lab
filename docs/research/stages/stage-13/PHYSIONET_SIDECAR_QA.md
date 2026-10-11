# PhysioNet EEG sidecar inventory: independent QA

Date: 2026-10-11. Verdict: **PASS**, limited to the PI-approved `RECORDS` and
`SHA256SUMS.txt` inventory under DEC-084. This is not source admission,
endpoint validation or Stage 13 protocol pre-freeze QA.

The independent reviewer parsed every rendered line of the official
[RECORDS](https://physionet.org/files/eegmmidb/1.0.0/RECORDS) and
[SHA256SUMS.txt](https://physionet.org/files/eegmmidb/1.0.0/SHA256SUMS.txt)
views. They independently found 1,526 unique expected `S001`–`S109` ×
`R01`–`R14` EDF paths, 3,058 unique valid checksum rows comprising those
1,526 EDF paths, 1,526 `.edf.event` companions and six ancillary paths.
No expected path or companion was missing. The checksum list's published
`RECORDS` digest matches the [audit packet](PHYSIONET_SIDECAR_AUDIT.md).

QA identified an early attribution error: exact byte counts were said to be
on the landing page, which displays rounded sizes. The packet was corrected
to the publisher's 25.3 KB and 253.8 KB display values before final QA;
the reviewer then returned `PASS`. Raw sidecar/member hashes, member existence,
signal/channel/time validity, subject independence, rights obligations and
safe splits were not verified. QA read no EDF header or signal, `.event`
content, archive, Electricity/test or model output and edited no tracked file.

The 1,526 paths are dependent runs within 109 listed subject IDs, not 1,526
independent subjects. Source/use, role, split, H-01 held-out count and
protocol-v3 freeze remain `HOLD`. Stage 09 `HOLD`/final QA `FAIL` and DEC-070
release `STOP` remain unchanged.
