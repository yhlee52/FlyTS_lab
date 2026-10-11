# Stage 13 non-human open-license candidate screen

Status: **metadata-only Director screen; independent QA pending; no source
admission or deeper access**. Prepared 2026-10-11 under DEC-092/093. Three
non-human sources were screened from official publisher landing and linked
rights/schema documentation. Search-result snippets were not treated as
source evidence. No archive, sidecar, sample table, signal, array, label,
test/Electricity item or model score was opened or downloaded.

## Fixed question

The encoder's pretrain-seen channel counts are 11 and 26. A primary held-out
H-01 paired count endpoint needs genuine concurrent signal channels from the
same independent original record, including a seen-count reference. Above-26
extrapolation requires at least 27 genuine channels. Repeated days, batches,
measurements, windows and seeds do not manufacture independent source
entities. A publisher's open-access badge alone does not identify the data
reuse license. These are screening rules, not a change to the Stage 11
contract or a source admission.

| Official source | Publisher-stated facts | Eligibility inference and unresolved items | Proposal |
|---|---|---|---|
| [UCI Gas Sensor Array Temperature Modulation](https://archive.ics.uci.edu/dataset/487/gas%2Bsensor%2Barray%2Btemperature%2Bmodulation) | CC BY 4.0; one described 14-MOX-sensor gas-chamber platform; 13 daily text files, 14 resistance columns plus time/conditions, 3.5 Hz resistance sampling, no missing values stated, 174.8 MB archive. Humidity/temperature references have their own 5-second cadence. | Fourteen genuine synchronous resistance channels might permit an 11-to-14 diagnostic, but cannot give a 26-channel reference or above-26 count. Thirteen days are repeated operation of the described platform, not 13 independent rigs. Actual continuity, rights notice, raw hashes and usable targets remain unverified. | `HOLD` for limited diagnostics; **reject as the current primary H-01 count remedy**. |
| [UCI Gas Sensor Array Drift at Different Concentrations](https://archive.ics.uci.edu/dataset/270/gas%2Bsensor%2Barray%2Bdrift%2Bat%2Bdifferent%2Bconcentrations) | One described 16-chemical-sensor array, 13,910 measurements across 10 batch files. Released rows contain 128 **features aggregated from sensor-response transients** plus gas/concentration information. **Rights conflict:** the page's description says research-only use, no commercial use and two required article citations, while its license panel says CC BY 4.0 permits any purpose with credit. | The 128 columns are feature summaries, not 128 concurrently sampled channels; the page describes one row per measurement rather than a released 256-point raw time axis. Batches and measurements are not independent arrays. Thus neither >26 genuine channels nor the required same-record temporal view is established. The conflicting use statements also fail the clear-rights screen. | **Reject for the current H-01 temporal count endpoint; source/use HOLD for rights conflict**. |
| [Zenodo Smart Factory Model Predictive Maintenance v1.0.0](https://zenodo.org/records/19242538) | Publisher record marks a 1.9 GB XML-based temporal case-base dataset as open and links underlying project resources. | The viewed record does not state a record-specific reuse license in its rendered Rights section, genuine concurrent channel count, independent machine/entity inventory, cadence or missingness. Zenodo's general default license cannot establish this record's exact terms. Source and endpoint eligibility remain unverified. | `HOLD`; no file access or source-use proposal. |

## Decision implication

**None of these three publisher-document screens supports a full H-01 count
freeze or source admission.** UCI Temperature Modulation has an explicit
CC BY panel, but its channel/entity limits remain. UCI Drift has conflicting
use terms on one official page; the Zenodo record's open badge lacks a visible
record-specific license. Both fail the clear-rights screen. This is a negative
screen of three named sources,
not a claim that no suitable open dataset exists. No ranking used model
performance, and no numeric threshold, seed, matrix or compute envelope was
changed to compensate.

PhysioNet source/use and its stopped contact path remain `HOLD`; the two
previously screened UCI human-activity candidates receive no automatic
admission. Appliances/Beijing and Bike keep their existing roles. Electricity
and all test signals/scores remain sealed. H-04 is `not tested`; Q2/Q3 are
unavailable. Stage 09 `HOLD`/final QA `FAIL` and report hashes, and DEC-070
public-release `STOP`, are unchanged. Stage 13 protocol-v3 freeze and Stage 14
handoff remain `HOLD` on current evidence. Any further candidate search,
deeper source read or claim-scope change requires its own PI decision.
