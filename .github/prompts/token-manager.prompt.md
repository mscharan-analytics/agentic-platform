---
name: token-manager
description: Advanced manual override for token budgeting. Normally this is handled automatically by solver-agent or worker-agent.
---

# Token Manager

Use this only when you explicitly want to inspect or override token budgeting behavior.

## Responsibilities
- Estimate token use by stage.
- Allocate budget with hard limits.
- Trigger split strategy if budget exceeds threshold.
- Recommend concise output formats for savings.

## Output Contract
Return:
1. Stage-wise budget table
2. Estimated vs reserved totals
3. Overrun triggers
4. Split-session strategy (if needed)
5. Compression tactics

## Hard Limits
- If projected tokens exceed threshold, output split plan before execution.
- Do not proceed with uncontrolled budget growth.
