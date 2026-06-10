---
name: session-closeout
description: Create and persist a concise session summary so future chats start with business and repo context without re-scanning everything.
---

# Session Closeout

Run this at the end of each chat/session.

## Required Actions
1. Generate concise summary from the current session.
2. Update `.github/context/summaries/SESSION-LATEST.md`.
3. Optionally append dated entry in `.github/context/summaries/` for history.
4. Keep only reusable context; remove noise.

## Output Contract
Return:
- summary_written: true/false
- target_files_updated
- carry_forward_context (bullets)
- next_session_start_prompt

## Required Summary Fields
- session_id
- date
- user_goal
- decisions
- repos_touched
- risks_or_gaps
- next_best_actions

## Guardrails
- No secrets
- No large logs
- No duplicate verbose analysis
