# Stage 13 specialist-budget revision request

Status: **proposal for PI decision**, 2026-10-11. No new specialist has been
activated under this request. It changes neither dataset access nor compute.
The Director checked Charter consistency; independent review of this new
request awaits budget capacity and is not claimed as `PASS`.

## Why the current allowance is exhausted

The approved [Charter](CHARTER.md) limits Stage 13 to three specialists,
two concurrent agents and one follow-up per specialist. Three independent
read-only QA specialists were used for the Charter, metadata shortlist,
sidecar inventory and six-header gate/result reviews. Their permitted one
follow-up each was used. The six-header result QA checked documentation and
arithmetic **without refetching EDF bytes**. Source admission and pre-freeze
QA have not occurred.

The remaining Charter work needs distinct scientific checks: Data for rights,
original subject/group and split admission; Experiment for H-01–H-03 endpoints
and statistics; Program Integrator for gate, matrix and budget consistency;
and independent QA for source and final pre-freeze packets. The Research
Director cannot replace those independent reviews with self-attestation.

## Proposed bounded amendment

```yaml
agent_budget:
  default_mode: single_agent
  max_specialists: 6          # three used + at most Data, Experiment, Integrator
  max_parallel_agents: 2      # unchanged
  max_debate_rounds: 1        # unchanged
  max_followups_per_agent: 2  # one additional focused QA pass per used reviewer
  max_agent_report_words: 700 # unchanged
  user_approval_for_expansion: true
```

This is an **upper bound**, not automatic staffing. Activate Data only for a
separately approved named-source audit/admission; Experiment only when an
eligible endpoint packet can be designed; Integrator only for protocol/budget
gate review. Reuse existing QA reviewers for one additional narrow source
or pre-freeze review each. All research roles stay read-only, one code path
has one implementation owner, and no specialist delegates. Each additional
memo remains capped at 700 words; there is no GPU/data/compute authorization
in this amendment.

| PI decision | Effect |
|---|---|
| `GO` — proposed | Permit up to three additional conditional specialists and one more follow-up per existing reviewer; retain every source, split, protocol and compute gate. |
| `REVISE` | Specify a lower staffing or follow-up ceiling; the Director resizes the pending source/protocol work and QA plan before activation. |
| `HOLD` | Continue Director-only tracked-document work; no new specialist or independent source/pre-freeze QA, so admission and Stage 13 freeze stay `HOLD`. |

The immediately next source-signal access, source/use admission, role and split
are **not** requested or approved here. After a budget decision, a named
PhysioNet access/admission packet will state exact files, network/storage
cost, rights and future test exclusion before the PI decides those gates.
Electricity and all test signals/scores remain sealed; Stage 09 status/hashes
and DEC-070 public-release `STOP` are unchanged.
