# Stage 13 physical-device screen: independent document QA

Final verdict: **PASS for the bounded DEC-095 official-document screen and
Kelmarsh metadata access request**, 2026-10-11. This does not approve reading
either proposed CSV, admit a source, assign a role/split or freeze protocol.

The independent reviewer checked that the screen names exactly three sources.
The [ENGIE-derived Mendeley record](https://data.mendeley.com/datasets/vmyg4yp3s8/2)
supports four turbines, 34 parameters and a processed CC BY deposit, while
original-owner rights and native channels remain `HOLD`. The [EDP owner
2016](https://edp.com/en/innovation/data/wind-farm-1-wind-turbine-scada-signals-2016)
and [2017](https://edp.com/en/innovation/wind-farm-1-wind-turbine-scada-signals-2017)
pages state CC BY-SA 4.0; the separately [deposited filtered record](https://data.mendeley.com/datasets/zjxjnjp3xs/2)
states four turbines, 83 columns and CC BY 4.0. The screen does not convert
those derived columns into native channels or the derived licence into the
owner's terms.

The [Cubico Kelmarsh record](https://zenodo.org/records/16807551) and
[official metadata API](https://zenodo.org/api/records/16807551) support six
turbines, partial-period signal availability, owner-stated CC BY 4.0,
record licence ID `cc-by-4.0`, and open access. The API file metadata matches
the proposed mapping CSV (3,150 bytes; MD5
`ca8fe399ab15ae7111d3214c632efd36`) and static CSV (807 bytes; MD5
`af3a038f0f7fddfc1608ad0bfc8cf5ba`). Their sum matches the requested
3,957-byte application-read cap. The reviewer opened **neither file**.

**Residual limits:** Original ENGIE owner rights/page, genuine concurrent
per-turbine channel counts, CSV contents/hashes, independent periods and
usable splits remain unverified. The principal regression risks are counting
four aggregates or 83 derived columns as native channels, treating turbines
or years as independent farms, or reading listed files before PI `GO`.
Stage 13 freeze is `HOLD`; Stage 09 history, H-04 `not tested`, sealed
Electricity/test and DEC-070 release `STOP` remain unchanged. This was a
document-only review, with no source data, model or evaluation access.
