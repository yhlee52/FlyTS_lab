# Proposed Kelmarsh mapping/static metadata access gate

Status: **two-file metadata access GO, DEC-096; one bounded execution
completed and its 3,957-byte cap exhausted**. Prepared under the
DEC-095 official-document screen. This approval does not admit Kelmarsh,
assign a role/split or change Stage 13 freeze `HOLD`.

Execution and independent conditional QA are recorded in
`KELMARSH_METADATA_AUDIT.md` and `KELMARSH_METADATA_AUDIT_QA.md`. The
prospective wording below records what the PI approved at the time; it is
not continuing permission for another read.

## Exact candidate and purpose

The source-owner [Cubico Kelmarsh v4 record](https://zenodo.org/records/16807551)
states six physical turbines, 10-minute SCADA data and CC BY 4.0 reuse.
The [official record metadata API](https://zenodo.org/api/records/16807551)
lists the following two small publisher files. **Only record metadata has
been read so far; neither file content has been accessed.**

| Exact published filename | Published size | Published MD5 | Why read |
|---|---:|---|---|
| `Kelmarsh_WT_dataSignalMapping.csv` | 3,150 bytes | `ca8fe399ab15ae7111d3214c632efd36` | Count distinct named native signals and flag status, setpoint, duplicate aggregate or derived columns; do not infer actual simultaneous completeness from the mapping alone. |
| `Kelmarsh_WT_static.csv` | 807 bytes | `af3a038f0f7fddfc1608ad0bfc8cf5ba` | Verify physical turbine IDs and common-farm grouping stated on the landing page. |

If PI approves, read exactly these two current-v4 source files from the
record into memory, with a **3,957-byte combined application-read cap** and
no unbounded retries. Check the exact byte lengths and MD5 against publisher
metadata before parsing; record any mismatch and stop. Emit only field-name,
turbine-ID and count summaries with evidence hashes; keep source contents out
of Git. Any unexpected redirect, larger response, hash mismatch or file
identity ambiguity is `HOLD`, requiring a new PI decision before retry.

No SCADA archive/member, annual ZIP, measurement value, signal time series,
event content, label, test/Electricity item, model score, download to disk,
training or evaluation is requested. The two CSVs cannot prove 27 *usable
concurrent* channels or independent farm-level evidence. A later bounded
non-test signal audit, rights/admission, role and split each require separate
packets, independent QA and PI decisions. Electricity and target tests stay
sealed; H-04 remains `not tested`, Stage 13 freeze remains `HOLD`, and
DEC-070 public release `STOP` remains.

## PI decision

- Mapping/static file access: **GO**, DEC-096, exact scope above.
- Source/use admission: **pending** (not decided by this request).
- Role and split: **pending** (not decided by this request).
