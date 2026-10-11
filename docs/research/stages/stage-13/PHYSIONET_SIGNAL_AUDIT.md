# PhysioNet EEG v1.0.0: six-file audit-only signal screen

Status: **bounded eligibility finding; source admission and H-01 remain
`HOLD`**. The PI authorized six in-memory EDF streams (DEC-087), fixed all
three inspected subjects as audit-only (DEC-088), and granted one same-file
retry after an incomplete first attempt (DEC-089). This packet records the
successful retry, not a formal evaluation or a corpus-wide adequacy verdict.
Independent [Data review](PHYSIONET_SIGNAL_AUDIT_DATA_REVIEW.md) found the
aggregate internally consistent for an audit-only packet (`GO with limits`).
Independent source/admission QA is pending.

## Access and provenance

On 2026-10-11 UTC, Windows 10 / Python 3.14.5 ran
`tools/stage13_physionet_signal_audit.py` at Git
`0a97232f76c755a765ebc59bb47c87dcca77e276`; its execution worktree
SHA-256 was
`d94132c7c3e5dac52ff9fbdb1a6b4d3eef09341f45301fc33378ac1d2e8235ff`.
The script re-read the previously authorized official
[`SHA256SUMS.txt`](https://physionet.org/files/eegmmidb/1.0.0/SHA256SUMS.txt)
sidecar in memory, then made one HTTP 200 GET for each of the six predetermined
members at `https://physionet.org/files/eegmmidb/1.0.0/`. It required the
exact member URL, no redirect, identity encoding, exact `Content-Length`
and hard per-file receive size. The six application-read EDF byte counts sum
to **11,515,296**, exactly the DEC-089 additional cap; HTTPS overhead was
not measured. The progress log ended at `11,515,296/11,515,296`. The first
interrupted attempt's EDF bytes remain unknown, so combined application-read
EDF bytes across both attempts could be as high as 23,030,592.

All six received full-member SHA-256 values match the publisher's listed
digests. Full-file hashing necessarily processed annotation bytes
cryptographically; the parser decoded only the 64 EEG signal channels and
did not decode or retain annotation values. No `.edf.event` file was opened.
No EDF, raw signal array, sample values, model output or checkpoint was
saved. The ignored aggregate-only JSON report is
`outputs/stage13_physionet_signal_audit.json`, SHA-256
`9680a249e739250e9d18f725f2b7c44f17156014ec7be83a1b53c566e71bc309`;
the ignored exclusive retry marker remains in place.

| Approved member | Bytes | One-second records | EEG samples/channel | Publisher SHA-256 matched |
|---|---:|---:|---:|---|
| `S001/S001R01.edf` | 1,275,936 | 61 | 9,760 | `4743b736131a7e147c150e8b37711029b6cda5e356c4b3e8261a03cdcaaf8b0c` |
| `S001/S001R03.edf` | 2,596,896 | 125 | 20,000 | `3427c8d01bff1380bc9ab9f27a35ece2af5dfadf3e291bbc05eb66e4dadbfe2e` |
| `S055/S055R01.edf` | 1,275,936 | 61 | 9,760 | `38df022c18db1a69e74261fefd85f397b0b55b457384c4c7208ef00f7f6231c6` |
| `S055/S055R03.edf` | 2,555,616 | 123 | 19,680 | `5a700147e53e7659c57d78b15dc2590378d5549edc35631fd7302c7847c5569c` |
| `S109/S109R01.edf` | 1,255,296 | 60 | 9,600 | `4547299bf4645e4afb08006d03b419e1273d4a3e853b8aa73d569e5a96dce8d0` |
| `S109/S109R03.edf` | 2,555,616 | 123 | 19,680 | `e2adb0517ec78e1ea79e6dbc7aba14f16b56243b8dafe630ad57deec29b79d34` |

## Fixed quality and paired-view checks

The six parsed headers each declare the same 64 ordered EEG labels (header
label digest `408d6576054f7ae71c71fbd35f35d63341a2a436b4d63f254fb733f8f161dc46`),
one annotation descriptor last, `uV` EEG physical unit, 160 EEG samples
per one-second record and 80 annotation samples per record. Full-file sizes
and per-record payload lengths agree. These are header/payload consistency
facts; EDF sample bytes carry no independent acquisition timestamps.

Across the **553 one-second records** and **88,480 time coordinates per EEG
channel**, the parser examined 5,662,720 EEG digital values. All scaled
values were finite and all digital values were within their declared ranges; there
were 74,481 exact digital zeros, zero declared digital-rail hits and zero
out-of-range values. Zero was **not** interpreted as missing. These
mechanical checks do not establish absence of artifacts, true missing
semantics, signal fidelity or suitability for a model.

For each run, the fixed header-order nested prefixes of 11, 26 and 64 EEG
channels have the same number of simultaneously mechanically valid time
coordinates as that run's samples/channel: 9,760, 20,000, 9,760, 19,680,
9,600 and 19,680 respectively. This shows that **same-record paired views
with a shared first-11-channel coordinate set are mechanically constructible
in these six audit-only recordings**. No model target, loss, corruption
metric, threshold or endpoint was calculated or chosen.

## Independent units, rights and next gate

The six runs belong to **three original subject IDs**, not six independent
subjects; within-subject runs and windows are dependent. All three subjects
remain excluded from pretraining, formal development evidence and every
final/test set under DEC-088. The remaining 106 listed subjects and 1,520
other EDF members were not signal-audited or assigned roles. Cross-subject
independence, domain shift, subject-disjoint split-before-windowing,
time/purge policy and train-only preprocessing are unverified.

The [official dataset page](https://physionet.org/content/eegmmidb/1.0.0/)
reports open access and ODC-By v1.0 and requests the dataset DOI
`10.13026/C28G6P` plus the original Schalk et al. (2004) BCI2000 paper.
The [license text](https://physionet.org/content/eegmmidb/view-license/1.0.0/)
distinguishes database rights from possible individual-content/privacy
rights and specifies notice for public use. Rights in individual EEG
contents, attribution/notice handling and any later public use require a
separate admission packet. The audit-only result supports
considering a source/role/split proposal; it does **not** admit PhysioNet,
provide an independent held-out H-01 count result, satisfy Stage 13 protocol
v3 freeze, or establish Q1/Q2/Q3. H-04 remains `not tested`. Electricity and
all test signals/scores stayed sealed; Stage 09 `HOLD`/final QA `FAIL` and
DEC-070 public-release `STOP` remain unchanged.
