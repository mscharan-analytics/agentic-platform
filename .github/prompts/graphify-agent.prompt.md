---
name: graphify-agent
description: Design graph-based orchestration for multi-agent execution using graph nodes, transitions, retries, and observability.
---

# Graphify Agent

Use this command when workflow orchestration requires branching, retry logic, or recoverable transitions.

## Graph Strategy
Use Graphify patterns (or equivalent) when:
- multiple dependent branches exist
- retries and compensating actions are required
- run state must survive interruptions

Reference implementation inspiration:
- https://github.com/safishamsi/graphify

## Output Contract
Return:
1. Node list with contracts
2. Edge/transition rules
3. Retry and backoff policy
4. Error transitions and recovery nodes
5. Execution trace schema

## Node Contract Template
- `node_id`
- `purpose`
- `inputs`
- `outputs`
- `on_success`
- `on_failure`
- `max_retries`
