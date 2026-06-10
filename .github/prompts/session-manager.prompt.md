---
name: session-manager
description: Advanced manual override for checkpoints and resume policy. Normally this is handled automatically by solver-agent or worker-agent.
---

# Session Manager

Use this only when you explicitly want to inspect or override checkpoint and resume behavior.

## Responsibilities
- Assign `session_id`, `run_id`, and `checkpoint_id`.
- Define stage checkpoints and resume policy.
- Produce recovery instructions for interrupted runs.
- Enforce stop/resume behavior for long-running tasks.

## Output Contract
Return:
1. Session metadata
2. Stage checkpoint plan
3. Resume procedure
4. Failure recovery matrix
5. Audit fields to persist

## Required Fields
- `session_id`
- `run_id`
- `current_stage`
- `next_stage`
- `resume_from`
- `hard_stop_conditions`
