---
name: worker-agent
description: Direct implementation command for code changes, verification, and completion without manually invoking manager prompts.
agent: worker-agent
argument-hint: Describe the implementation task and constraints
---

Use this when the task is already clear and execution should start immediately.

Required behavior:
- Absorb context-management, token-management, and session-management internally.
- Do not tell the user to call helper manager prompts.
- Make focused edits, verify them, and finish the task end-to-end when possible.

Return compactly:
1. Work completed
2. Verification result
3. Remaining risk or blocker