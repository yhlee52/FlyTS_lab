# Token and Context Budget Policy

## Default budget

Every stage charter declares a budget. Unless the user approves otherwise:

```yaml
agent_budget:
  default_mode: single_agent
  max_specialists: 3
  max_parallel_agents: 2
  max_debate_rounds: 1
  max_followups_per_agent: 1
  max_agent_report_words: 700
  user_approval_for_expansion: true
```

The Codex project config caps open spawned-agent threads separately. This policy is stricter: available capacity is not permission to use it.

## Delegation gate

Before spawning, the primary Research Director records:

- the independent question;
- why the primary agent should not answer it alone;
- the files or evidence the specialist needs;
- the maximum useful output;
- the stop condition.

If those fields are unclear, do not delegate.

## Context packets

Send a specialist only:

1. goal and assigned question;
2. relevant paths or source links;
3. confirmed constraints and decisions;
4. required output structure and length;
5. explicit stop condition.

Do not forward full chat history, old lab meetings, unrelated logs, or the intended answer. Rebuild context from canonical repository artifacts.

## Output compression

- Return conclusions and evidence pointers, not search diaries.
- Store long logs under ignored `outputs/` paths.
- Cap normal specialist memos at the role file limit.
- Allow one rebuttal only when it changes a material decision.
- Resolve continued disagreement with a small experiment or user decision.
- Replace stale notebook state rather than appending narrative history.

## Model effort

- Use demanding reasoning for Research Director, Architecture, Experiment, and QA only when the task is genuinely complex.
- Use a lighter model for narrow context, status, source/schema, and traceability work when appropriate.
- Do not use a speed tier as a cost-saving mechanism.

## Escalation

Stop and ask the user before exceeding the charter budget, adding a new standing role, running a second full-lab round, or expanding the stage scope.
