# Kelmarsh v4 two-file metadata audit

Status: **bounded DEC-096 access completed; independent QA CONDITIONAL PASS;
source/use, role, split and Stage 13 freeze remain HOLD**. Executed on
2026-10-11 from branch base `18db297c4695da6173797ef5d8cccd7e2de70aaa`
with Python 3.14.5. The executed worktree script was
`tools/stage13_kelmarsh_metadata_audit.py`, SHA-256
`0e738854eaf69b4a4196f67ec44fcf72bfce9ff813d0a287649dd016529460da`.
Its four synthetic `unittest` cases passed before the source read. The
repository's ordinary Python lacked `pytest`; no package was installed.

## Exact access and byte evidence

The script made one request each to the two exact Cubico Kelmarsh v4
[Zenodo record](https://zenodo.org/records/16807551) metadata-file URLs,
read source bytes **only in memory**, required HTTP 200, exact final URL,
declared `Content-Length`, identity encoding and published MD5, and stopped
after **3,957 application bytes**. It saved no source content or model output
to disk. No other source file, SCADA ZIP/member, measurement value, array,
test/Electricity item or score was opened.

| Official filename | Application bytes | Publisher MD5 | Local SHA-256 of verified source bytes |
|---|---:|---|---|
| `Kelmarsh_WT_dataSignalMapping.csv` | 3,150 | `ca8fe399ab15ae7111d3214c632efd36` **matched** | `2dad8552ba4d45d59b9a778c68025b8c3614179d48dfb938c3af07c90ebd06af` |
| `Kelmarsh_WT_static.csv` | 807 | `af3a038f0f7fddfc1608ad0bfc8cf5ba` **matched** | `a249919471580244d41a547e407ef371d45f2d5347a59bc23cf3c980f607ee93` |

The application-byte count excludes HTTP headers and transport buffering;
it is the cap named in the PI request. No repeat access has occurred.

## Parsed metadata summaries

- The mapping CSV has **60 rows** and columns `Greenbyte Signal ID`,
  `Greenbyte Title`, `Manufacturer Title`, `Unit`. Each of the three name/ID
  columns has 60 nonempty, distinct values; `Unit` is nonempty in 57 rows
  with 14 distinct nonempty unit strings. The extractor emitted the 60 IDs
  but **did not emit title values**, so this audit cannot classify status,
  setpoint, duplicate aggregate or derived entries.
- The static CSV has **6 rows** and 14 columns. `Identity`, `Title`,
  `Alternative Title`, latitude and longitude each have six distinct values;
  `Wind Farm`, manufacturer and model each have one distinct value. The
  extractor reported distinct counts but **did not emit turbine ID values**.
  This verifies six distinct rows within one farm at the metadata level,
  without establishing independent farms or periods.
- The 60 `Greenbyte Signal ID` values were emitted to the execution tool
  transcript, although the decision requested only field-name, turbine-ID
  and count summaries. They were not committed or saved as a source file and
  are not measurements. Whether these values fall within "field-name" is
  ambiguous; this audit treats their emission as a **possible output-scope
  deviation**, does not reuse them, and makes no eligibility inference from
  them. The omission of actual signal titles and turbine IDs is an extractor
  defect reproduced by independent QA with a synthetic fixture.
- Sixty mapping entries are **not** 60 genuine simultaneously observed
  per-turbine channels. No annual SCADA header, missingness, target mask,
  paired 11/26/>26 view, or split was audited. H-01 count remains `HOLD`.

## Boundary and next evidence

The executed summary did not fully meet the request's planned semantic
classification and exact turbine-ID listing. The approved 3,957-byte cap
has been exhausted, so no second read will occur under DEC-096. A corrected
extractor and a **new PI access decision** would be needed to read the
3,150-byte mapping again for titles or 807-byte static file for exact IDs.
Even that would be metadata, not proof of concurrent usable channels; a
separately approved bounded non-test SCADA audit and source/use, role and
split admission would still be necessary. No checkpoint, evaluation result
or compute budget is inferred from this audit. H-04 remains `not tested`,
Q2/Q3 unavailable, Electricity/test sealed, Stage 09 history untouched, and
DEC-070 public release `STOP` in force.

Independent QA reviewed the access controls and synthetic checks, but did
not replay Zenodo access. The byte counts and hash matches above are
Director-reported execution evidence, not independently observed network
evidence. See `KELMARSH_METADATA_AUDIT_QA.md`.
