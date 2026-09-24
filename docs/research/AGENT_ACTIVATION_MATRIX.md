# Agent Activation Matrix

Custom agents are a capability pool, not a standing meeting. Default to the primary agent alone and activate the smallest useful set.
`Director` means the primary Codex agent, not a spawned custom agent. Every other role is a bounded specialist subagent.

| Stage | Default active roles | Conditional roles |
|---|---|---|
| 0 — baseline reproduction | Director, Implementation, QA | Program Integrator |
| 1 — protocol | Director, Program Integrator, Experiment, QA | Architecture |
| 2 — channel masking | Director, Architecture, Implementation, QA | Data, Experiment |
| 3 — robustness evaluator | Director, Experiment, Implementation, QA | Data |
| 4 — topology modularization | Director, Architecture, Implementation, QA | Experiment |
| 5 — topology controls | Director, Architecture, Experiment, QA | Implementation |
| 6 — corpus v1 | Director, Data, Implementation, QA | Program Integrator |
| 7 — conventional baselines | Director, Architecture, Implementation, Experiment, QA | Program Integrator |
| 8 — pilot | Director, Experiment, QA | Implementation, Data |
| 9 — formal study | Director, Experiment, QA, Program Integrator | Architecture, Data |
| 10 — v0.1 release | Director, Program Integrator, QA | relevant specialists |

## Activation rules

Activate a role only when at least one is true:

- the question requires distinct domain expertise;
- an independent check materially reduces a high-impact risk;
- independent work can proceed without duplicating the same context;
- a stage charter explicitly requires the role.

Do not activate a role for a trivial edit, formatting, an already-decided issue, or a question another active role already owns.

## Meeting levels

- **Micro review:** Director plus one relevant specialist and QA. Default for bounded changes.
- **Full lab review:** Director, Program Integrator, QA, and relevant specialists. Reserve for architecture selection, dataset admission, experiment protocol, pilot interpretation, formal conclusions, and release.
