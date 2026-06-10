# Agent Routing Rules

Use a linear execution model in this repository.

## Default Behavior

- Prefer a single primary entrypoint per user request.
- Use `solver-agent` when the request needs framing, routing, planning, or repo analysis.
- Use `worker-agent` when the request is already clear enough to execute.

## No-Circle Policy

- Do not send the user through chains of helper prompts.
- Do not bounce between `solver-agent`, `worker-agent`, `agent-intake`, `problem-router`, `token-manager`, `context-manager`, and `session-manager`.
- Apply token, context, and session controls internally unless the user explicitly asks to inspect or override them.
- Visible handoffs should be minimal and directional.

## Handoff Rules

- `solver-agent` may hand off to `worker-agent` when execution is ready.
- `worker-agent` should finish the task directly and should not hand control back to `solver-agent` unless a real blocker prevents safe execution.
- If a blocker exists, ask the smallest possible clarifying question instead of redirecting the user through more commands.

## Escalation

- Use specialist prompts only when they produce a distinct deliverable the user explicitly wants.
- Avoid routing loops, repeated intake, or repeated planning summaries.
- Prefer action and completion over orchestration chatter.