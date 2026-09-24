# FlyTS Decision Log

## DEC-001 — Public data first

- Date: 2026-09-24
- Decision: Validate the generic representation model on public multivariate time-series data before semiconductor transfer.
- Evidence: project consensus and development plan
- Rejected alternative: semiconductor-specific first implementation
- Revisit when: FlyTS-Mini v0.1 stage gate is complete

## DEC-002 — Channel input is a set

- Date: 2026-09-24
- Decision: Do not bind the generic backbone to a fixed channel count or channel order.
- Evidence: target public domains and semiconductor recipe variability
- Rejected alternative: dataset-specific fixed channel projection
- Revisit when: metadata-aware identity is designed

## DEC-003 — Human stage gates

- Date: 2026-09-24
- Decision: The user approves stage scope, PR merge, and advancement.
- Evidence: requested advisor/customer operating model
- Rejected alternative: autonomous continuous stage advancement
- Revisit when: user explicitly changes governance

## DEC-004 — Concise shared notebook

- Date: 2026-09-24
- Decision: Agents share `CURRENT_STATE.md` and evidence links instead of full conversation transcripts.
- Evidence: token budget and context-quality requirements
- Rejected alternative: forwarding complete history to every agent
- Revisit when: a concrete handoff failure shows missing context

## DEC-005 — Selective agents

- Date: 2026-09-24
- Decision: Maintain a seven-role capability pool but activate only the smallest useful subset.
- Evidence: subagents duplicate model/tool work and coordination cost
- Rejected alternative: full-lab activation for every task
- Revisit when: stage retrospectives show insufficient independent review

## DEC-006 — Human alignment and ambiguity gate

- Date: 2026-09-24
- Decision: Stop and ask the user at material decision gates or whenever multiple plausible interpretations would change the work; agent consensus does not substitute for user intent.
- Evidence: explicit user request after reviewing the Agent/Skill/Harness design
- Operating rule: present options, recommendation, and impacts; treat no response as `HOLD`; record explicit "you decide" delegation
- Rejected alternative: agents resolving ambiguous requirements internally and reporting only the final conclusion
- Revisit when: the user explicitly changes the desired oversight level
