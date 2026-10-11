# PhysioNet EEG v1.0.0: source/use decision gate

Status: **HOLD — DEC-092 stopped the PhysioNet clarification path** in favor
of clearly reusable open sources. The earlier DEC-091
[inquiry draft](PHYSIONET_RIGHTS_INQUIRY_DRAFT.md) remains unsent and is no
longer a pending action.
This is a PI decision packet, not an admission or permission for further data
access. The six-file [audit](PHYSIONET_SIGNAL_AUDIT.md) and independent
[source-result QA](PHYSIONET_SIGNAL_AUDIT_QA.md) establish only bounded
technical readiness. A read-only Data specialist follow-up recommended
source/use `HOLD`; it is not legal clearance or a formal role/split review.

## Facts, inference and unresolved condition

- The [official version 1.0.0 page](https://physionet.org/content/eegmmidb/1.0.0/)
  lists the dataset as open access under ODC-By v1.0 and requests three
  citations: Schalk's dataset DOI `10.13026/C28G6P`, Schalk et al. (2004)
  BCI2000, and the standard PhysioNet citation (Pollard et al., 2026).
- PhysioNet's [About page](https://physionet.org/about/) additionally requests
  its Goldberger et al. (2000) citation for publications using PhysioNet data.
- The [ODC-By terms](https://physionet.org/content/eegmmidb/view-license/1.0.0/)
  grant database rights subject to conditions. Sections 2.4 and the preamble
  say individual contents may carry separate copyright, privacy or data-
  protection rights that this license does not cover. Sections 4.2–4.3 set
  notice conditions for public database conveyance and public use of a
  produced work.
- **Inference:** limited internal research use is plausible from the open
  listing, but the two pages do not establish consent, ethics/de-identification
  status or independent permission for processing individual EEG recordings
  for FlyTS. Keeping work nonpublic does not by itself settle those rights.
  Therefore source/use admission is not supported on the present record.

## PI choices

| Choice | Effect |
|---|---|
| **A — seek written rights clarification (recommended)** | Keep source/use `HOLD`; request publisher/contributor clarification or an applicable institutional privacy/legal determination for the exact planned internal model-development use. No message is sent by the research agents without separate authorization. Resume admission review only when the answer is recorded. |
| B — use another candidate | Keep PhysioNet `HOLD`; start a new, separately approved source/role/split and access path for a candidate with clearer individual-content reuse conditions. |
| C — pause the source path | Keep PhysioNet and the Stage 13 protocol freeze `HOLD` pending a later PI direction. |

**Decision history:** DEC-091 selected A and produced an unsent inquiry.
DEC-092 superseded that next action; no external contact or admission follows.

If source/use is later approved, separately decide a development-held-out role
and an exact subject-disjoint split **before** opening any further signal.
S001/S055/S109 remain audit-only and excluded from pretraining, formal
development and all final/test use under DEC-088. The other 106 subject IDs
remain unassigned. A later access request must state exact members, byte and
storage bounds, official version/URL, publisher member hashes, retrieval date,
captured license/notice, source lock, citation plan and raw-data protection.
The six audited member hashes matched the publisher sidecar; the sidecar's
own raw-byte hash was not independently verified. No raw recordings, arrays
or checkpoints enter public Git, and any public output or redistribution
requires its own rights and DEC-070 release review.

H-01 count remains unfrozen; H-04 is `not tested`; Q2/Q3 are unavailable.
Electricity/test stay sealed. Stage 09 `HOLD`/final QA `FAIL` and report hashes
remain historical, and DEC-070 public-release `STOP` continues.
