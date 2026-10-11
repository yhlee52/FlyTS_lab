# Stage 13 high-channel non-human candidate screen

Status: **Director metadata-only screen under DEC-094; independent document
QA PASS; no source admission or deeper access**. See the
[QA record](HIGH_CHANNEL_OPEN_CANDIDATE_SCREEN_QA.md). Prepared 2026-10-11. The three named
sources below were checked using official publisher landing, rights, schema
or repository documentation only. No data member, sample row, array, signal,
label, test/Electricity item or model output was accessed or downloaded.

## Screening question

Pretraining used 11 and 26 channels. An independently held-out H-01 count
comparison needs genuine simultaneous channels on the same original record,
including a seen-count reference and an unseen view. An above-26 comparison
needs at least 27 such channels. This targeted screen also requires distinct
original entities and a clear license covering **data reuse**. Repeated
recordings, time windows, locations on one rig, or random seeds cannot by
themselves establish independent physical entities or domains. These are
screening criteria, not source admission or a claim about model performance.

| Named official source | Confirmed publisher statements | Missing or conflicting evidence; eligibility inference | Screen proposal |
|---|---|---|---|
| [UCI Gas Sensor Arrays in Open Sampling Settings](https://archive.ics.uci.edu/dataset/251/gas%2Bsensor%2Barrays%2Bin%2Bopen%2Bsampling%2Bsettings) | One 72-MOX-sensor chemical detection platform produced 18,000 recordings at six wind-tunnel locations; each measurement has 72 concurrent resistance traces of 260 s at 100 Hz. The license panel says CC BY 4.0. The same official description says use is exclusively for research and commercial use is excluded. | **Rights conflict:** the description's use restriction disagrees with the CC BY panel's unrestricted-purpose grant. Six locations and many recordings reuse the described platform and wind tunnel; they are not six independent rigs. The channel criterion is met, but independent entity and clear reuse rights are not. Raw hashes, usable paired targets and group/time separation remain unverified. | **Source/use HOLD** for rights conflict; reject as the current independent held-out H-01 remedy. No source-file access. |
| [Harvard Dataverse Additional Tennessee Eastman Process Simulation Data](https://doi.org/10.7910/DVN/6C3JR1) ([official metadata API](https://dataverse.harvard.edu/api/datasets/export?exporter=dataverse_json&persistentId=doi%3A10.7910%2FDVN%2F6C3JR1)) | The dataset-level `termsOfUse` contain a public-domain dedication for lawful use, with no-endorsement and amendment terms. The description states 55 table columns: fault number, simulation run, sample index, then 52 process variables at a three-minute cadence. Simulation run indexes 1-500 represent different random-generator states; training and testing seeds are stated to be non-overlapping. Four RData files are listed, separated into fault-free/faulty training/testing. | A 52-variable simultaneous process view is plausible, but the metadata does not establish which variables are observed signals versus manipulated/control values or that a valid same-target 11/26/>26 nested view exists. The 500 runs are **synthetic trajectories of one plant model**, not 500 physical plants or independent held-out domains. File-level schema, usable targets and any more specific notices remain unverified. The live landing page required browser verification; the official metadata API was accessible and its `termsOfUse`, description and file-name fields were checked without accessing file contents. | Candidate for a **separate PI source-document/access request** limited to non-test metadata if the PI accepts a synthetic-process claim scope; no admission or H-01 freeze now. |
| [NetManAIOps OmniAnomaly Server Machine Dataset](https://github.com/NetManAIOps/OmniAnomaly) ([LICENSE](https://github.com/NetManAIOps/OmniAnomaly/blob/master/LICENSE)) | The publisher README says 28 machines in three groups, 38 dimensions, five weeks of data and a per-machine earlier-half train/later-half test. The repository has an MIT LICENSE whose operative text applies to "software and associated documentation files." | The README does not establish a data-specific redistribution/reuse grant from the collecting Internet company. A public repository and code MIT license do not settle that question. Independence across machines and common infrastructure, channel semantics, timestamps, clean development split, file hashes and rights remain unverified. The publisher's existing test half stays sealed. | **Source/use HOLD** pending explicit data rights; no access or admission. |

## Decision implication

No candidate has all three targeted conditions **confirmed** from the allowed
documents. UCI has enough genuine channels but one described rig and
contradictory use statements. Harvard's explicit public-domain language makes
it the clearest rights lead, but its trajectories share one simulated process
model; any claim would have to state that scope, and its variable semantics
still need a gated audit. SMD has multiple named machines and 38 dimensions,
but no confirmed data-specific license. This is a bounded negative/partial
screen of three named candidates, not evidence that suitable open data do not
exist. No candidate is admitted, assigned a role/split or ranked by scores.

The PI must separately decide whether to request Harvard's non-test schema and
terms, seek another bounded candidate search, propose a narrower hypothesis/
claim contract, or keep Stage 13 at `HOLD`. None of those paths is automatic.
PhysioNet source/use and contact path remain `HOLD`; existing approved roles
are unchanged. Stage 13 protocol/compute freeze and Stage 14 handoff remain
`HOLD`; H-04 is `not tested`, Q2/Q3 unavailable, Electricity and all test
signals/scores sealed, and DEC-070 public release `STOP` remains. Stage 09
`HOLD`, final QA `FAIL` and report hashes are untouched.
