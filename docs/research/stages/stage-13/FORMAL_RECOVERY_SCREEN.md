# Stage 13 formal recovery: bounded new-source metadata screen

Status: **Director screen complete under DEC-117; independent bounded result
QA `CONDITIONAL PASS`** ([review](FORMAL_RECOVERY_SCREEN_QA.md)).
Screen date: 2026-10-13 (Asia/Seoul). This is a publisher-document screen,
not source admission, source-file access, a protocol freeze or a model result.

## Authorization and method

The PI approved the exact [request](FORMAL_RECOVERY_SEARCH_REQUEST.md): eight
queries in order, the first five results of each used query, at most three
previously unscreened non-human official landing pages and two linked official
rights/schema documents per source. Search snippets selected pages but were
not used as evidence. The third page was selected at query 4, result 1, so
queries 5–8 were not issued. No dataset file, sidecar, preview, sample row,
archive, signal, label, test/final item or model output was accessed or
downloaded. No previously screened source was reopened.

| Query used, in approved order | First-five disposition in result order |
|---|---|
| 1. `open multivariate sensor time series dataset license channels` | 1 Paessler PRTG **selected**; 2 aquatic-drone data article **selected**; 3 OpenMarineStream describes one FerryBox-style system/nine streams, not multiple original devices; 4 NSF SAGE is a channel-code guide, not a named corpus; 5 RMISC is a compilation with source-specific rights, not an original source-owner record. |
| 2. `open multivariate sensor time series dataset entities schema` | 1 Palantir sensor schema documentation, not a public corpus; 2 Paessler duplicate; 3 OpenMarineStream duplicate; 4 W3C sensor ontology, not a corpus; 5 CMU teaching page describes four measured channels, below the 11-channel screen. |
| 3. `industrial machine sensor time series dataset license channels` | 1 Industrial Atlas catalog, not the source-owner record; 2 Database Sample page lists temperature/vibration/throughput only; 3 CIMEGS is a multi-source catalog without a named original corpus; 4 IoTDataset is a catalog rather than the owner record; 5 MetroPT-3 Industrial Atlas is a third-party catalog and describes one train compressor. |
| 4. `industrial machine sensor time series dataset entities schema` | 1 FactoryNet owner repository **selected**; stopped at three selected sources. Results 2–5 were not considered after the approved stop rule. |

The list is a bounded search trace, not a claim that other public sources do
not exist. Selection used only the apparent non-human, multichannel and
multiple-entity cues in those result titles/snippets; the opened publisher
pages determine the evidence status below.

## Official-page observations and eligibility

| Selected source; pages actually opened | Publisher-stated facts (`confirmed` at document level) | `unverified` or `conflict`; decision |
|---|---|---|
| [Paessler PRTG Open Dataset README](https://github.com/PaesslerAG/prtg-open-dataset/blob/main/README.md), [owner repository landing](https://github.com/PaesslerAG/prtg-open-dataset), [repository LICENSE](https://github.com/PaesslerAG/prtg-open-dataset/blob/main/LICENSE) | Paessler says about 20,000 series/80 million points from 15 installations for one month, typically at one-minute intervals. Its PRTG *sensor* channels are retrieved together, and company/sensor IDs are described. The repository shows a BSD-2-Clause LICENSE. | A query-wide 19-column example spans sensors and is **not** 19 simultaneous channels on one original sensor. No official page inspected states that any one sensor has 11 or 27 valid measured channels, their common observed targets, missingness, an eligible train/development split or independent installations. The LICENSE text calls its subject “software”; whether the grant covers the measurement data is `unverified`. No source/use, role or split admission. |
| [PMC aquatic-drone article archive](https://pmc.ncbi.nlm.nih.gov/articles/PMC7118297/) | **None independently confirmed from the page.** The article archive returned only a browser challenge during the authorized open. | The search snippet's plural drones and multivariate signals were selection cues only. The archive could not establish an owner/publisher dataset landing page, so this selection does not meet the intended provenance screen. Rights, actual device/entity count, simultaneous channels, cadence, missingness and split are all `unverified`. No linked source document was opened or replacement selected. |
| [FactoryNet owner repository](https://github.com/Forgis-Labs/FactoryNet), [LICENSE](https://github.com/Forgis-Labs/FactoryNet/blob/main/LICENSE), [official documentation folder](https://github.com/Forgis-Labs/FactoryNet/tree/main/docs/workshops/poster-icml2026) | The owner describes 23,000+ task episodes across six embodiments, real and simulated material, and a 24-signal schema. Its S/E/F/C groups distinguish commanded setpoints, efforts, measured feedback and context. The owner states CC BY-NC-SA 4.0 for the release. | The 24 schema signals cannot be counted as 24 eligible measured feedback channels. Per-embodiment simultaneous measured-channel count, missingness, original machine/site independence, split/purge and data provenance/licence of each underlying contribution are `unverified`. Six embodiments and 23,000 episodes are not six independent factories. The noncommercial/ShareAlike conditions need source/use review; no admission. |

`Confirmed` means the linked owner/publisher page states the fact, not that
source bytes or statistical independence were checked. No inspected source
has documented the full rights + at-least-11 concurrent measured channels +
independent held-out unit + leakage-safe split combination. Even a nominal
11/27 count would still need separately authorized source and paired-target
audits. The aquatic article's blocked page is an access/provenance limit, not
negative evidence about the dataset.

## Result and next gate

This screen provides **no Stage 13 eligibility or H-01 paired-count
admission**. Keep protocol v3, low/medium/high compute choice, pre-freeze QA,
PI Stage 13 `GO` and formal Stage 14 at `HOLD`. The single DEC-117 read-only
independent result QA returned `CONDITIONAL PASS`, with the audit limits
recorded in its report. The PI may decide whether a **new, exact**
source-document/file access request is justified or
to retain `HOLD`; the current search approval cannot be reused or widened.
No contract narrowing is inferred.

Appliances/Beijing and Bike keep their approved roles/splits. Kelmarsh and
PhysioNet exclusions are unchanged. Electricity and every target-test
signal/score remain sealed. H-04 is `not tested`; Stage 09 `HOLD`/final QA
`FAIL` and report hashes, DEC-112–115 engineering execution `HOLD`, Stage 15
`NO GO`, and DEC-070 public-release `STOP` remain in force.
