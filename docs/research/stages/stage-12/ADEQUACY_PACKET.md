# Stage 12 adequacy packet — approved existing sources

Status: bounded evidence accepted by independent QA and PI under DEC-078/079.
Date: 2026-10-11. No model training, evaluation, test-signal read, final opening,
or new source admission is part of this packet.

## Access and evidence boundary

DEC-075 approved the Charter. DEC-076 approved bounded local archive, notice,
source-lock, manifest, and prepared **train/validation** signal/mask reads for
Appliances, Beijing and Bike. DEC-077 approved reading the shared manifest and
notice metadata solely for these three sources. Electricity raw/prepared/final
signals and model scores, all target-test signals, and HAR/HARTH raw data were
excluded. The canonical local manifest is
`data/stage06-public-v1-r2/manifest.json`, SHA-256
`44bafe48196a4afd096e387dc672cad128d390ab7e5b413ea6cbeadf5f3e7f6c`.
Other local manifests are earlier variants and are not substituted for it.

The tracked Stage 06 result and `reports/data/stage06-corpus-v1.json` are the
historical baseline. Stage 09 remains `HOLD` with final QA `FAIL`; its evidence
and hashes are unchanged. Stage 11 defines a qualification contract, not an
empirical result. DEC-070 continues to stop public release.

## Corpus identity, time and independence

| Source | Existing role | Split records train/val/test | Original entities | Entity-by-split time regions | Prepared channels and cadence | Independence limit |
|---|---|---:|---:|---:|---|---|
| Appliances | pretrain | 1/1/1 | 1 (`energydata_complete`) | 3 | 26; 600 s | One chronological source entity across splits. |
| Beijing | pretrain | 12/12/12 | 12 stations | 36 | 11; 3,600 s | The same 12 stations recur across splits; no unseen-station claim. |
| Bike | development-held-out | 71/1/6 | 1 (`hour`) | 3 | 4; 3,600 s | Train fragments and validation are one source entity; 71 train records are not 71 independent entities. |

These counts come from approved-source rows of the canonical manifest, checked
against the tracked Stage 06 report. Source ranges are chronological and
disjoint; the validation and test regions begin 512 source points after their
respective partition boundaries. Bike's many contiguous fragments arise from
timestamp discontinuities **within** its train/test partitions. They do not
increase independent entity count. Windows, augmentations and seeds are not
independent sampling units. Beijing's stations share a city and time period,
so treating all 12 as statistically independent would need a later dependence
analysis; the manifest proves distinct station IDs, not independence.

A bounded read of the 98 approved train/validation `.npy` files found 98/98
SHA-256 and shape/dtype matches to the manifest. Nonfinite source entries were
0/0 for Appliances train/validation, 55,533/6,800 for Beijing, and 0/0 for
Bike, matching the tracked Stage 06 report. Every approved train/validation
record had at least one finite value in every channel, although Bike includes
very short train fragments unsuitable for many window contexts. These counts
describe source missingness and do not measure artificial dropout. All three
sources include finite zero values, so zero must not be read as missing. The
manifest has no separate mask path; `src/flyts/corpus.py` derives observation
masks from finiteness at window read time.

`src/flyts/prepare.py` converts numeric source columns directly to float32,
retains source `NaN`, splits each original entity chronologically before
windowing, applies a 512-point partition purge and cuts timestamp gaps into
records. `src/flyts/corpus.py` builds windows inside those records. No fitted
cross-record normalization is applied by that conversion path. The separate
evaluation reference statistics in `src/flyts/evaluation.py` use visible,
non-target coordinates of each view; a future protocol must preserve that
target-exclusion rule. No claim of unseen-entity generalization follows from
the current chronological split.

The converter excludes Appliances' `date`, `rv1`, and `rv2` from signals;
Bike's ID/calendar/categorical fields and `casual`/`registered` shortcut
components are excluded while `cnt` remains a source channel; Beijing's
timestamp/station fields and categorical wind direction are excluded. Timestamps
come from each source's date/hour fields, not from a signal channel. Beijing's
source `NA` denotes missingness; the other two approved train/validation
arrays are finite. Exact prepared channel order is bound in each manifest row.

## Provenance and rights checks

| Source | Official source / local archive | Notice and source-lock check | Status |
|---|---|---|---|
| Appliances | [UCI dataset 374](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction); `data/raw-public-v1/appliances.zip` | Archive SHA matches source lock and canonical manifest; no bundled notice entry in the prepared notice file | archive confirmed; rights subject to UCI landing-page terms and QA |
| Beijing | [UCI dataset 501](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data); `data/raw-public-v1/beijing.zip` | Archive SHA matches source lock and canonical manifest; no bundled notice entry in the prepared notice file | archive confirmed; rights subject to UCI landing-page terms and QA |
| Bike | [UCI dataset 275](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset); `data/raw-public-v1/bike.zip` | Archive SHA matches source lock and canonical manifest; bundled `Readme.txt` requires citing Fanaee-T and Gama (2013) in publications | archive/notice confirmed; rights subject to UCI terms and QA |

Archive SHA-256 values, in table order, are
`2fccf354445d886e7917620b0195db1f3e3e34d5a067a93b844694a4c561255a`,
`b04da438b2f331ac0ffd45aebdfec0d20d2367feb5f6948c4b1f7ce1191e33c4`,
and `b70182d0d0508e9abbb79306ce5c0cec34869000f8220175ac83d11dbe845401`.
Member names and exact SHA-256 values are recorded under the three approved
`sources[*].member_sha256` entries of the canonical manifest.

The manifest's source metadata records UCI CC BY 4.0 landing-page terms. The
three opaque archive SHA-256 values match `data/raw-public-v1/sources.lock.json`
and the canonical manifest. The Data specialist independently matched expected
member hashes as opaque bytes without reading test-range values. The prepared
notice file contains no bundled Appliances or Beijing notice and contains
Bike's README citation condition. The Director checked all three official UCI
pages on 2026-10-11; each explicitly states CC BY 4.0. Appliances' UCI page also
says permission was obtained to distribute the merged third-party weather data.
The specialist had recommended rights `HOLD` while relying on the unsigned
local source lock alone; the direct UCI-page check resolves that narrow gap.
Independent QA and the PI still decide source use. Preserve attribution and
Bike's publication citation.

Bike's source `temp`, `hum` and `windspeed` are already normalized before the
FlyTS converter reads them; the converter does not fit their scale on the FlyTS
train split. **Bike `temp` physical semantics are in conflict:** the bundled
README says the values were divided by 41, while the current official UCI page
says they use `(t - (-8))/(39 - (-8))`. Stage 12 cannot choose one definition
from the prepared values or infer Celsius values safely. Keep the exact
temperature inverse/unit interpretation `conflict` until authoritative source
clarification; future protocol claims must either avoid that interpretation or
resolve it before use. No additional cross-split fitted preprocessing was found
in the Stage 06 converter.

## H-01 / H-02 view feasibility, before any model score

The current manifest has **pretrain train** channel counts 11 (Beijing) and 26
(Appliances), derived by the `seen_channel_counts` rule in
`src/flyts/evaluation.py`. These are the only current nominal training-seen
counts; no empirical generalization is inferred from them.

| Source/split | H-01 paired nested count view | Permutation | H-02 0/10/30/50% channel dropout | Claim limit |
|---|---|---|---|---|
| Appliances validation | Mechanically possible within one 26-channel entity for some unseen counts between/below 11 and 26; the bounded first-window mask check found common observed targets. | Channel/mask permutation possible. | The bounded first-window check supports nonempty paired targets at all proposed rates. | Same entity as pretrain train; diagnostic only. |
| Beijing validation | At most 11 source channels; lower-count extrapolation candidates can pair with 11 on the same station. The bounded first-window check found common observed targets; interpolation above 11 cannot be tested here. | Channel/mask permutation possible per station. | The bounded first-window check supports nonempty paired targets; source NaNs remain distinct from artificial dropout. | Twelve seen stations, not station transfer. |
| Bike validation | **Unavailable under the current evaluator's paired rule.** Its 4 channels cannot supply the nearest seen 11-channel view, so all candidate count rows are skipped. | Four-channel permutation is mechanically possible. | Four-channel dropout is possible in principle; 10% can round to zero removed channels and needs an effective-view check. | One independent entity; cannot establish H-01 breadth or entity-level uncertainty. |

The count-view rule in `src/flyts/evaluation.py` requires both unseen and nearest
seen counts on the **same original window**, with common observed target
coordinates and a shared visible reference. Since Bike has 4 channels and the
nearest seen count is 11, synthetic padding cannot repair the missing paired
observation. A count available only on a pretrain entity is a within-source
diagnostic, not held-out domain evidence. Permutation must move signals and
masks together. Dropout comparisons must retain the same record, target and
reference coordinates; a zero-removal 10% view is an identity, not evidence of
10% corruption. No Q2 channel coverage or robustness threshold is asserted.

As a **feasibility check only**, each approved validation record's first 128
source points were examined with the current candidate 8-point patch geometry.
The number of fully observed patches was 16/16 for Appliances, 12–16/16 for
each of Beijing's 12 stations, and 16/16 for Bike. A candidate 40% temporal
mask selects six of 16 valid patches, leaving common observed target and
reference patches even at Beijing's minimum of 12 fully observed patches.
This establishes existence of paired coordinates in those records, not an
executed evaluator fixture, model score or future frozen view count. On Bike,
all four channels are observed in the first validation window, but no 11-channel
paired count view exists. Its 10% dropout arm can still round to zero removed
channels; effective arm coverage needs a later preregistered fixture audit.

## H-04 admission packet status

No new target source access or admission was approved. HAR retains its original
README usage-rights conflict. HARTH retains its missing bundled notice,
S006's observed 10 ms cadence versus the 50 Hz description, and absent official
class 14 in the fixed candidate test split. Neither is repaired by changing a
seed, split or metric after inspecting coverage. No raw candidate or test-label
array was opened. Every H-04 candidate therefore remains `HOLD` pending a
candidate-specific rights/ontology/group/class/test packet and PI decision.
Without an admitted target, H-04 is `not tested` and Q2/Q3 are unavailable.
This does not itself block separately approved Electricity-only readiness.

| Candidate | Rights/notice | Label/task ontology | Independent groups and class coverage | Target-local train/validation and sealed test | Admission |
|---|---|---|---|---|---|
| HAR | Original README conflicts with UCI rights label | Existing activity labels are tracked, but rights gate is unresolved | No new Stage 12 group/coverage audit approved | No target-local run; test sealed | `HOLD` |
| HARTH | Bundled notice absent | Fixed official activity-code set; no post-hoc relabeling | S006 cadence conflict; fixed candidate test lacks class 14 | No target-local run; test sealed | `HOLD` |
| New candidate | No source approved | unverified | unverified | unverified | `HOLD` until a source-specific packet and PI gate |

## Proposed PI decisions, not approvals

| Source | Source/use recommendation | Role proposal | Split proposal | Needed decision or evidence |
|---|---|---|---|---|
| Appliances | Propose `admit` for existing bounded source use after QA/PI; broader independent-entity claim `HOLD` | Keep pretrain | Keep chronological split for bounded diagnostics; no unseen-entity claim | PI decides continued source/use and role/split separately. |
| Beijing | Propose `admit` for existing bounded source use after QA/PI; unseen-station claim `HOLD` | Keep pretrain | Keep chronological split; no unseen-station claim | PI decides continued source/use and role/split separately. |
| Bike | Propose `HOLD` for H-01 count coverage and physical `temp` interpretation; bounded dimensionless development diagnostics may remain possible | Keep development-held-out | Keep existing split; no coverage-driven re-search | PI decides whether this limited use is acceptable or more data are required. |
| Electricity | No adequacy judgment | Keep sealed final-held-out | No change | Final-data/score opening remains outside Stage 12. |
| HAR / HARTH | HOLD | No H-04 role | No split change | Candidate-specific rights and fixed-split evidence required. |

The proposal table itself granted no admission and changed no role or split.
Each PI decision names the source, allowed use, role, split identity and
excluded claims. A missing decision remains `HOLD`.

**PI disposition (DEC-078):** Appliances and Beijing each received `admit` for
the existing bounded use with their current `pretrain` role and canonical r2
chronological split. Bike received only bounded, dimensionless development
diagnostic use with its current `development-held-out` role and split; H-01
paired-count coverage and physical `temp` interpretation remain `HOLD`. These
decisions create no new registry or manifest version because roles and splits
were retained. Electricity and H-04 sources received no new admission.

## Stage 13 handoff inputs and open questions

Approved local archive bytes: Appliances 11,979,507; Beijing 8,192,212; Bike
279,992. Approved **train/validation** prepared `.npy` bytes: 1,691,504;
15,469,248; 237,376 respectively. These are storage/I/O inputs only, not
an approved compute envelope. The manifest provides source lengths, channel
counts, cadence and entity/record counts; a later protocol can estimate window
processing after selecting context/stride and hardware. It must not use window
counts as independent sample size.

Additional evidence needed: an independently held-out source with at least a
seen channel count for H-01 paired count comparisons, broader independent
entities for H-02 uncertainty, and a rights-cleared H-04 target with ontology,
group-separated target-local train/validation and sealed test class coverage.
Stage 13, after its own PI gate, must decide thresholds, inference and multiple
comparison rules, seeds, matrix, compute envelope, and checkpoint selection.
This Stage 12 packet fixes none of them.

## Local reproducibility preflight finding

The tracked Stage 06 role registry's canonical LF bytes have SHA-256
`0095d4cd76ad5fdaeefeccdbb4322187892cc155bfac619ca4c8618ea50b9b20`,
matching the report. The current Windows checkout converts that file to CRLF
(`git ls-files --eol`: `i/lf w/crlf`), producing worktree SHA-256
`705124ddc5646889c4f2609747d1627ece383344fd540b8ee9c641685cfb6adc`.
The loader checks raw bytes, so a local corpus-loading preflight would fail on
this checkout despite an unchanged Git blob. This is a reproducibility risk
for Stage 13; it is not evidence that the source registry or historical report
changed. No tracked code/config was altered to resolve it.
