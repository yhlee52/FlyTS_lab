---
name: flyts-lab-notebook
description: Maintain FlyTS's concise shared research memory in docs/research without copying chat transcripts or raw logs. Use after a material decision, experiment, PR, QA result, risk change, stage handoff, or whenever an agent needs to refresh CURRENT_STATE.md, hypotheses, decisions, risks, evidence, or stage results for future agents.
---

# Maintain the FlyTS Lab Notebook

Preserve only durable research state. Prefer precise links and evidence over narrative history.

## Route updates

- Always refresh `docs/research/CURRENT_STATE.md` after material work.
- Update hypotheses, decisions, risks, and traceability only when their state changes.
- Write stage QA and result files when the stage is reviewed or closed.

Keep `CURRENT_STATE.md` at or below 150 lines. Do not paste chat transcripts, full logs, stack traces, or long diffs. Replace stale details instead of appending a diary. Link to evidence and mark unverified claims `미검증`.

Maintain exactly these headings: `Current stage`, `Current goal`, `Canonical references`, `Confirmed decisions`, `Open questions`, `Active risks`, `Latest evidence`, and `Next action` as level-two headings.

Validate from the repository root:

```bash
python .agents/skills/flyts-lab-notebook/scripts/check_notebook.py
```

Report only which notebook records changed and why.
