---
name: agent-intake
description: Single intake command that classifies the problem and routes to solver-agent or worker-agent without requiring manual manager commands.
---

# Agent Intake

Use this only if the user explicitly wants routing help. The normal front door is `/solver-agent`.

## Input
- Problem statement
- Optional constraints (deadline, risk, production impact, repos)

## Output Contract
Return exactly:
1. Problem type
2. Primary command
3. Why that command fits
4. Internal controls to auto-apply
5. Execution order
6. Follow-up questions (0-4, only if required)

## Routing Policy
- Prefer `/solver-agent` for intake, analysis, planning, and orchestration.
- Prefer `/worker-agent` for direct implementation when scope is already clear.
- Treat token, context, and session management as internal controls, not user-facing requirements.
- Do not produce circular command chains. Recommend one primary command and at most one direct follow-on command.
- If confidence is high, do not ask questions.
- If blocked/ambiguous, ask 1-4 concise verification questions.

## Default Sequence
1. `/solver-agent`
2. `/worker-agent` if implementation is required

Do not recommend manager prompts in the default path.

## Internal Controls

The selected primary command should absorb these controls automatically when needed:
- context-management
- token-management
- session-management
- problem-routing
