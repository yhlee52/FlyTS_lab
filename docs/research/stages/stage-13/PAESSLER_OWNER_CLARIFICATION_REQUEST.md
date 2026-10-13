# Stage 13 formal recovery: one Paessler owner clarification request

Status: **PI `GO` (DEC-118); posting failed, no issue created**
(2026-10-13). Stage 13 remains
`HOLD` and formal Stage 14 remains `NO GO`. DEC-117's search and result-QA
allowance is spent. This proposal creates a new, separate permission boundary.

## Decision requested

Authorize the Research Director to post **one public GitHub issue** in
`PaesslerAG/prtg-open-dataset`, using the exact title and body below, and to
read **at most the first substantive owner/maintainer reply** in that issue.
This is a metadata clarification only. If GitHub Issues is unavailable, the
post fails, or no owner reply arrives, stop without another channel, issue,
comment or follow-up. No independent QA staffing is requested at this step.

| PI choice | Effect |
|---|---|
| `GO` (recommended) | Permit that one public issue and one owner-reply read only. |
| `REVISE` | Change the exact wording, public channel or cap before any contact. |
| `HOLD` | Send nothing; retain Stage 13 and formal Stage 14 at `HOLD`. |

The PI selected `GO` on the exact Draft PR #38 request. At 2026-10-13
14:14 UTC, the GitHub integration rejected the single create-issue call for
`PaesslerAG/prtg-open-dataset` with HTTP 403, `Resource not accessible by
integration`. No issue URL or sent text exists; no owner reply was read.
The stated failure rule stops this route. No alternate account, channel,
post, comment, or retry was used. A new PI decision would be required to
change the delivery route.

## Why this candidate and this limit

The bounded [DEC-117 screen](FORMAL_RECOVERY_SCREEN.md) found a Paessler owner
repository describing channels retrieved together and 15 installations, but
the repository's BSD-2-Clause LICENSE refers to software. The existing pages
do not establish a grant for measurement-data reuse, at least 11 concurrent
measured channels on one original sensor, or independent held-out units. These
are early rejection questions under the unchanged Stage 11 H-01/Q1 contract.
FactoryNet's 24-signal schema mixes commands, feedback and context; its full
count is not an eligible measured-channel count. The aquatic article archive
was inaccessible. No source is admitted. A single owner question avoids a
new dataset-file read or another open-ended source search.

## Exact public issue

**Title:** PRTG Open Dataset: measurement-data terms and sensor-channel metadata

**Body:**

> We are checking whether the public PRTG Open Dataset could be used in a
> multivariate time-series research benchmark. We need only documentation or
> aggregate metadata, not data files or sample rows. Could a maintainer clarify:
>
> 1. Does this repository's BSD-2-Clause LICENSE apply to the measurement
>    time-series data, including research use and publication of aggregate
>    results? If different terms apply, could you link to them?
> 2. Does the released dataset include any *one original PRTG sensor* with at
>    least 11 simultaneously measured channels sharing timestamps? Separately,
>    are there any with at least 27? Please distinguish channels of one sensor
>    from columns aggregated across sensors, and link to an existing channel
>    schema or mapping if available.
> 3. Are the 15 installations distinct original collection units, and are
>    there documented dependencies among them that would prevent treating an
>    installation as a held-out unit? We do not need installation identities.
>
> Please do not post raw traces, sample rows, private identifiers or
> unpublished material. A link to existing public documentation is enough.

The issue must not name FlyTS, claim dataset eligibility, request private data,
or make a licensing conclusion on the owner's behalf. Record the issue URL,
UTC timestamp and exact sent text. An owner reply is publisher-stated evidence,
not proof of paired target coverage, independent sampling or source admission.

## Stop and later gates

If rights do not cover data or the owner cannot identify a same-sensor
11-channel case, close this recovery branch at Stage 13 `HOLD` without
accessing source files. If the answer is affirmative but incomplete, prepare
a separately bounded source access and independent QA packet; do not use this
issue as approval for downloads, raw/prepared reads, source/use, role, split,
protocol v3, compute, model execution, Stage 14 or PR merge. The PI must
decide each later gate. No reply or an ambiguous reply is `HOLD`, not consent.

Kelmarsh and PhysioNet decisions remain unchanged. Electricity and all
target-test signals/scores remain sealed; H-04 is `not tested`. Stage 09
`HOLD`/final QA `FAIL` and report hashes, DEC-112-115 engineering execution
`HOLD`, Stage 15 `NO GO` and DEC-070 public-release `STOP` continue.
