# SINGLE WORKER PROTOCOL

## Operating model

There is one worker only: GPT-6.1 Sol. The user assigns work to that worker after the planner has prepared the phase in `PLAN.md`. No agent sends the assignment to another chat on the user's behalf without a new explicit instruction.

The worker must not:

- spawn subagents;
- replace the phase order;
- modify planner-owned environment files; record a proposed change for the planner instead;
- treat AI-created templates, scripts, or JSON indexes as authoritative;
- access or mutate external systems when a read-only local check is enough;
- include secrets in output.

The worker may change implementation artifacts when the current assignment allows it. Examples are `tools/`, `knowledge_base/templates/`, derived indexes, drafts, and audit reports.

## Required worker loop

1. Read `AGENTS.md`, `PLAN.md`, and the rules relevant to the phase.
2. Inspect the current files before editing.
3. Make the smallest change that satisfies the phase.
4. Run meaningful checks and preserve their output or a concise result.
5. Report changed files, evidence, tests, unresolved risks, and a suggested next step. Return the report to the user; do not start the next phase.

## Environment ownership

The planner owns the AI environment:

- `AGENTS.md`;
- `GEMINI.md`;
- `PLAN.md`;
- `.agents/rules/`;
- `.agents/skills/`.

If the worker discovers a needed environment change, it records a proposal in its report. The planner applies and reviews that change before the next assignment.

## Reporting standard

Distinguish inspected files from tested behavior. Use Critical/High/Medium/Low for issue severity and P0–P4 only for phase IDs. Include test command, result, artifact path and limitations. Lack of source access is an unresolved verification item, not a successful audit.
