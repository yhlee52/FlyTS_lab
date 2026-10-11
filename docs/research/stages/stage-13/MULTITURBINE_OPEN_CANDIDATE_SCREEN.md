# Stage 13 physical-device open-data candidate screen

Status: **Director document-only screen under DEC-095; independent QA PASS;
no source admission or deeper access**. See the
[QA record](MULTITURBINE_OPEN_CANDIDATE_SCREEN_QA.md). Prepared 2026-10-11. Exactly three
named wind-farm sources were screened through official source-owner or
repository landing, rights and schema descriptions. No archive, source CSV,
sample row, array, signal, label, test/Electricity item or model output was
opened or downloaded.

## Eligibility boundary

Pretrain-seen counts are 11 and 26. An above-26 H-01 count view requires at
least 27 genuine concurrent measurements on the **same original turbine
record**, paired to a seen-count reference and common observed target. Four
statistics (mean/min/max/SD) of one measurement do not automatically become
four independent channels. Different turbines are original physical devices,
but turbines in one farm share weather, operation and time; neither 10-minute
rows, years, windows nor seeds are independent farms. All named source role,
split and test decisions remain separate PI gates.

| Named source and official documentation | Confirmed document facts | Unverified or conflicting evidence and screen outcome |
|---|---|---|
| **ENGIE La Haute Borne**: [Mendeley publisher record v2](https://data.mendeley.com/datasets/vmyg4yp3s8/2), which credits the former ENGIE source | The third-party deposited record describes four named physical MM82 turbines, 34 process parameters per turbine at 10-minute intervals, with mean/min/max/SD aggregates. It labels its processed 2013-2018 deposit CC BY 4.0 and says the original ENGIE dataset is no longer online. The former ENGIE open-data hostname did not resolve during this screen. | **Source/use HOLD.** The deposited licence and reprocessing description do not prove the original owner's authorization for this particular redistribution or define the resulting independent native channels. The original publisher page, native schema and archive rights cannot be verified from the allowed documents. No file access or count claim. |
| **EDP Wind Farm 1**: [owner 2016 page](https://edp.com/en/innovation/data/wind-farm-1-wind-turbine-scada-signals-2016), [owner 2017 page](https://edp.com/en/innovation/wind-farm-1-wind-turbine-scada-signals-2017), [Mendeley derived-record description](https://data.mendeley.com/datasets/zjxjnjp3xs/2) | EDP's two year-specific pages explicitly license their wind-turbine SCADA datasets under **CC BY-SA 4.0**, with GMT time zone. A separate researcher-deposited, filtered Mendeley record describes four named turbines, 83 columns per turbine, 10-minute intervals and a CC BY 4.0 label. | **HOLD for 27-channel eligibility and any derivative use.** The original EDP pages do not specify native per-turbine signal count or actual concurrency. The 83 derived columns cannot be counted as 83 original channels without a schema audit. The derived deposit's CC BY label differs from the owner pages' ShareAlike terms; it is not a substitute rights basis. Original EDP source/use and file access need separate review. |
| **Cubico Kelmarsh v4**: [owner-deposited Zenodo record](https://zenodo.org/records/16807551), [official metadata API](https://zenodo.org/api/records/16807551) | Cubico identifies six physical Senvion MM92 turbines and 10-minute SCADA/events data for 2016-2024, with some signals absent in some periods. Cubico explicitly states **CC BY 4.0** release; the record metadata licence ID is `cc-by-4.0`, access is open, and publisher archive/checksum metadata are listed. The record lists a 3,150-byte signal-mapping CSV and an 807-byte static-turbine CSV; only their **names, sizes and posted MD5s** were read. | **Best bounded metadata lead, not admitted.** The landing page does not state how many genuine simultaneously observed per-turbine signals survive exclusions for status, setpoints, duplicate aggregates and missing periods. Six turbines share one farm/weather regime, and usable independent periods, targets, hashes and a sealed split remain unverified. Access to either listed CSV is a new source-file gate. No signal or count endpoint freeze. |

## Gate implication

Kelmarsh is the strongest screened lead with an owner-stated open data
licence, multiple physical devices and a clear mapping-file listing. The
**at-least-27 true concurrent channels condition remains unverified** for
all three. This is a partial screen, not admission or statistical evidence.
The next smallest useful step is a candidate-specific PI request to read only
Kelmarsh's published 3,150-byte mapping and 807-byte static CSV, verify their
publisher MD5s and determine whether a later bounded non-test SCADA audit is
worth proposing. The mapping/static contents have **not** been read. Any
archive, member, train/development signal, role or split would need a later
separate decision. EDP/ENGIE are not silently substituted if Kelmarsh fails.

The PI may approve that exact metadata-file request, choose another named
route, propose a narrower claim contract or leave Stage 13 at `HOLD`.
Current protocol/compute freeze and Stage 14 handoff remain `HOLD` until
source, role and split admission plus valid paired-count evidence. H-04 is
`not tested`, Q2/Q3 unavailable, Electricity/test signals and scores sealed,
Stage 09 historical `HOLD`/final QA `FAIL` unchanged, and DEC-070 public
release `STOP` remains.
