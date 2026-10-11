# Stage 13 held-out count source: metadata-only shortlist

Status: screening only; independent document-only QA `PASS`, 2026-10-11
([review record](CANDIDATE_SHORTLIST_QA.md)). No candidate access, admission,
role, split or protocol freeze decision. Prepared under the Stage 13 Charter
(DEC-082) and the PI's bounded official-page discovery `GO` (DEC-083).

## Question and screening rule

The current pretrain-seen channel counts are 11 and 26. Bike has four channels
and one original entity; it cannot supply a same-record 11-channel reference
for the current H-01 count comparison. This search asks whether an independent
held-out public source *might* supply at least 11 genuine, concurrent channels
and, for above-seen extrapolation, at least 27. Channel totals on publisher
pages establish only nominal potential. Actual common observed targets,
sampling, independent groups, lawful use and a leakage-safe split require a
separately approved source audit. No performance result informed this list.

`Confirmed` below means reported by the official publisher page, not
independently verified against source bytes. `Unverified` blocks admission.
There were exactly three candidate sources in this search. No source archive,
sidecar inventory, sample table, signal, label, test item or model score was
read or downloaded.

## Publisher metadata

| Candidate and official source | Confirmed publisher facts | Inference relevant to H-01/H-02 | Unverified or conflicting eligibility |
|---|---|---|---|
| [PhysioNet EEG Motor Movement/Imagery v1.0.0](https://physionet.org/content/eegmmidb/1.0.0/) | 64 EEG channels, EDF+ recordings at 160 Hz; subject directories S001–S109; 14 runs are described per subject. The page lists Open Data Commons Attribution License v1.0 and an approximately 1.9 GB compressed archive. | 64 nominal EEG channels could form 11/26/>26 nested views within an original subject-run if the signal, channel order, time axis and common targets survive audit. Subject IDs are possible independent groups; runs/windows within a subject are dependent. | Complete usable subject/run inventory, EDF channel alignment, missing or bad channels, source/member hashes, notice obligations, subject/time overlap, feasible split and paired views. The page's event annotations vary in meaning by run; no label or H-04 task is admitted. |
| [UCI PAMAP2 Physical Activity Monitoring](https://archive.ics.uci.edu/dataset/231/pamap2%2Bphysical%2Bactivity%2Bmonitoring) | Nine subjects; three 100 Hz IMUs and an approximately 9 Hz heart-rate monitor. Of 54 columns, timestamp and activity label are not signals. The publisher flags four orientation columns in each 17-column IMU group as invalid. The page lists CC BY 4.0 and a 656.3 MB archive. | The 52 listed sensory attributes include one asynchronous heart-rate stream and 12 invalid orientation columns, leaving **at most 39 candidate same-rate IMU channels**. This arithmetic is a screening inference, not a valid-channel inventory. Subject-disjoint held-out views could be possible. | Actual valid concurrent channels, NaN patterns, sessions and original-group completeness, time alignment, archive/member hashes, bundled notice, rights conditions in use, split/purge and paired observed targets. Activity labels remain excluded; H-04 is not admitted. |
| [UCI Daily and Sports Activities](https://archive.ics.uci.edu/dataset/256/daily) | Eight subjects, five sensor units with 45 axes at 25 Hz. The page describes 19 activities and 60 files of 125 samples (five seconds) per subject/activity, 9,120 files total, no missing values, CC BY 4.0 and a 162.9 MB archive. | 45 nominal axes could span 11/26/>26. The 9,120 clips are **not** 9,120 independent subjects. At the existing 256-point context, a 125-point file alone is too short. | Channel validity, file ordering and whether the five-minute recordings can be reconstructed without gaps or overlap, source hashes/notice, usable independent groups, a lawful group/time split and paired observed targets. Altering context or stitching clips would be a separate protocol/source decision, not assumed here. Activity labels remain excluded; H-04 is not admitted. |

All three sources would be a *new* domain. Neither a nominal count nor a large
number of recordings makes it an admitted development-held-out domain. In
particular, multiple runs, clips, windows and seeds do not increase the number
of original subjects. Subject labels alone may not eliminate shared protocol,
device or temporal dependence; this must be audited before uncertainty or
cross-domain claims are specified. No candidate supplies Q1/Q2/Q3 evidence now.

## Proposed next decision: one minimal named-source access gate

**Recommendation for PI review:** permit a read-only inventory of just the
official PhysioNet `RECORDS` and `SHA256SUMS.txt` sidecars linked from its
[v1.0.0 publisher page](https://physionet.org/content/eegmmidb/1.0.0/).
These small source files would let Data/QA check listed subject-run members and
the publisher's archive/member checksum scheme before requesting the much
larger signal archive. The inventory would not establish signal validity,
same-record paired views, use admission or a split. Record the exact sidecar
URLs, access time and SHA-256 of bytes read in an audit packet if approved.

This proposed access explicitly excludes EDF headers and signal bytes, the
full archive, annotations/labels and all test/final data, as well as any
download into `data/`. No other candidate source file is requested. The PI may
instead choose PAMAP2 or Daily and Sports Activities for a separately scoped
source request, or put all candidates on `HOLD`. After an approved inventory,
any deeper source read or download, source/use admission, development role,
group/time split and seal still require their own PI decisions under the
Charter. The current H-01 held-out count endpoint and protocol-v3 freeze remain
`HOLD` throughout this metadata step.

## Boundary and inherited state

Appliances/Beijing remain pretrain; Bike remains dimensionless development
diagnostics with H-01 count coverage `HOLD`; Electricity and all test
signals/scores remain sealed. HAR/HARTH remain `HOLD`, H-04 is `not tested`,
and Q2/Q3 are unavailable. Stage 09 `HOLD`, final QA `FAIL` and report hashes
are unchanged. DEC-070 public release `STOP` continues.
