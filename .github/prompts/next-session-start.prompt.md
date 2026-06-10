---
name: next-session-start
description: Generate a one-shot starter prompt for the next chat using persistent project context and the latest session summary.
---

# Next Session Start

Use this command at the beginning of a new chat so you do not have to restate business context.

## Inputs
- Optional: `new_goal`
- Optional: `constraints`

## Data Sources (must read in this order)
1. `.github/context/PROJECT-CONTEXT.md`
2. `.github/context/summaries/SESSION-LATEST.md`

## Output Contract
Return exactly these sections:
1. Loaded Context Snapshot
2. Carry-Forward Decisions
3. Open Risks or Gaps
4. Suggested Command Stack
5. Ready-To-Paste Starter Prompt

## Ready-To-Paste Starter Prompt Template
Produce a final block the user can paste directly:

```text
Context loaded from PROJECT-CONTEXT and SESSION-LATEST.
Business context: <1-2 concise lines>
Carry-forward decisions: <bullets>
Known gaps/risks: <bullets>
New goal: <new_goal or inferred goal>
Constraints: <constraints or none>
Please proceed with the recommended command stack and ask up to 1-4 concise verification questions only if blocked.
```

## Rules
- Keep output concise.
- Do not include secrets.
- If `SESSION-LATEST.md` is stale or empty, state that and continue with project context.
