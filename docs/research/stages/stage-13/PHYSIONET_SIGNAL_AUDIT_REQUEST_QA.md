# PhysioNet signal-audit access request: independent document QA

Status: **PASS**, 2026-10-11. This is a read-only review of the proposed
access and audit-only exclusion gates, not a source-byte or scientific-result
QA. The reviewer edited no tracked files and read no EDF signal, annotation,
Electricity, test data or model output.

## Scope and finding

The six EDF paths match the predetermined sidecar and header pilot. Scope A
declares 11,515,296 full-file bytes, with a largest file of 2,596,896 bytes.
Scope B declares 553 records, 11,325,440 EEG bytes plus 101,376 header bytes,
and at least 565 planned range requests. The request now specifies exact
HTTP response checks, redirect/encoding rejection and hard receive caps.
Scope A discloses that annotation bytes transit but will not be decoded or
retained; scope B excludes annotation sample bytes. The audit-only restriction
keeps all three inspected subjects out of pretraining, formal development and
future sealed test, without admitting the remaining subjects or fixing a
formal split.

Data-specialist review first recommended revision for request arithmetic,
rights boundaries, subject dependence and deterministic quality checks. The
Director corrected the request. Independent QA then raised hard-cap,
predicate and cadence-wording defects; these were corrected before this
**PASS**. No blocker remains for a **PI decision on the request**.

## Unverified and required gates

Publisher member digests have not been recomputed. Sample validity, common
observed targets, subject independence and individual-content rights remain
unverified. The PI must separately approve an exact signal-access scope and
the S001/S055/S109 audit-only exclusion before any signal byte is read.
Source/use admission, development role, formal split, H-01 endpoint, protocol
and compute remain `HOLD`. This QA does not authorize execution or override
DEC-070 public-release `STOP`.

Reviewed: [access request](PHYSIONET_SIGNAL_AUDIT_REQUEST.md),
[header pilot](PHYSIONET_HEADER_PILOT.md),
[sidecar inventory](PHYSIONET_SIDECAR_AUDIT.md), Stage 13
[Charter](CHARTER.md), [budget amendment](AGENT_BUDGET_REVISION_REQUEST.md),
DEC-086 and `CURRENT_STATE.md`.
