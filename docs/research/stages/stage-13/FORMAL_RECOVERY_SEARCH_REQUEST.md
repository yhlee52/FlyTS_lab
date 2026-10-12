# Stage 13 formal recovery: new-source metadata screen request

Status: **proposed; PI decision pending** (2026-10-13). Stage 13 remains
`HOLD` under DEC-099/110. This request preserves the Stage 11 H-01/Q1
contract and does not activate formal Stage 14.

## Decision requested

Authorize **one** bounded, read-only search for at most **three previously
unscreened non-human public multivariate time-series sources**, plus **one
read-only independent QA follow-up** on the resulting screen. The QA staffing
allowance used for the earlier Stage 13 closeout and source screens is
exhausted; this follow-up needs its own PI decision. Approval of the search
does not approve any candidate's file access, source/use, role, split,
protocol, compute, model run, or Stage 14 entry.

| PI choice | Effect |
|---|---|
| `GO` (recommended) | Permit only the screen and one result QA described here; seek separate decisions for every later step. |
| `REVISE` | Set a different search or QA bound before any discovery. |
| `HOLD` | Perform no search; retain Stage 13 and formal Stage 14 at `HOLD`. |

## Why another screen is needed

The approved pretrain channel counts are 11 and 26. Bike has four channels
and one original entity, cannot provide a same-record 11-channel paired
count reference, and a nominal 10% dropout may remove zero channels.
Training-seen entities provide diagnostics, not independent held-out count
evidence. Prior official-page screens and the bounded Kelmarsh/PhysioNet
audits admitted no replacement source. Kelmarsh's 60 mapping title pairs,
six same-farm turbines, ZIP inventory and 2016 audit-only prefix do not
establish concurrent usable channels or independent held-out units. The
PhysioNet source/use and contact path remain `HOLD`. Reusing earlier search
or access caps would exceed their decisions.

## Exact search boundary

- Use these eight queries, in order, stopping once three sources are selected:
  `open multivariate sensor time series dataset license channels`,
  `open multivariate sensor time series dataset entities schema`,
  `industrial machine sensor time series dataset license channels`,
  `industrial machine sensor time series dataset entities schema`,
  `environmental monitoring multivariate sensors license channels`,
  `environmental monitoring multivariate sensors entities schema`,
  `physical device time series open data license channels`, and
  `physical device time series open data entities schema`. Search results and
  snippets are discovery aids, never evidence.
- Inspect at most three newly named source-owner/publisher landing pages and
  at most two official linked rights/schema/documentation pages per source.
  Record URL, access date, exact publisher assertion, and whether each item
  is `confirmed`, `unverified`, or `conflict`. Do not access repository data
  files, archives, sidecars, previews, sample rows, API data endpoints,
  mirrors, labels, signals, arrays, model outputs, or test/final material.
- Screen for an explicit **data-reuse** grant, genuine simultaneous measured
  channels on each original record (at least 11; prioritize at least 27 for
  above-26 extrapolation), multiple original entities with their common-site
  dependence visible, time/cadence and missingness, and a plausible
  group/time split with a sealed test region. A column total, feature
  aggregate, recording count, or repeated window is not a channel or an
  independent entity without evidence.
- Exclude all named sources in `CANDIDATE_SHORTLIST.md`,
  `OPEN_LICENSE_CANDIDATE_SCREEN.md`,
  `HIGH_CHANNEL_OPEN_CANDIDATE_SCREEN.md`, and
  `MULTITURBINE_OPEN_CANDIDATE_SCREEN.md` from this **new-source** round.
  No prior exclusion, rights conflict, or access decision is reversed.
- For each query, consider its first five results in rank order. Select the
  first three distinct official landing-page URLs whose result text plausibly
  names a non-human source, simultaneous channels and multiple entities;
  skip prior screened sources. Open only those three, with no replacement if
  an opened candidate fails the publisher-page screen. Record each selection
  and skip reason; do not rank by model performance. Stop after three pages
  or eight queries. If none is selected, record a negative bounded screen;
  do not infer that no suitable public source exists.

The output is one concise candidate table with official links, rights,
concurrent-channel and original-entity claims, dependence/split limits, and
missing evidence. One independent reviewer checks the search authorization,
source provenance, count/entity reasoning, exclusions, seal and claim limits
from those public pages and tracked records only. QA performs no source-file
read. The screen and QA cannot establish admission or paired-count validity.

## Subsequent gates, only if a candidate survives

Prepare a named, byte-bounded non-test source access request and pre-read QA
packet. After a separate PI access `GO`, audit rights/notice, source hashes,
native schema, same-time observed channels, original entities/dependence,
missingness, split/purge and same-record common targets for 11/26 and
interpolation/extrapolation views. Obtain distinct PI source/use, role and
split decisions. Only then prepare protocol v3, low/medium/high compute
envelopes, an exact freeze manifest, new independent pre-freeze QA staffing
and QA `PASS`, and PI protocol/budget `GO`. A formal Stage 14 Charter and
preflight have their own later gates. Failure at any eligibility or approval
step leaves Stage 13/formal Stage 14 at `HOLD`; changing Q1 requires a
separate Stage 11 contract decision.

Electricity and all target-test signals/scores remain sealed. H-04 is `not
tested`; Q2/Q3 are unavailable. Stage 09 `HOLD`/final QA `FAIL` and report
hashes, DEC-112~115 engineering execution `HOLD`, Stage 15 `NO GO`, and
DEC-070 public-release `STOP` are unchanged.
