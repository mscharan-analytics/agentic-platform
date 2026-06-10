---
name: context-manager
description: Advanced manual override for context shaping. Normally this is handled automatically by solver-agent or worker-agent.
---

# Context Manager

Use this only when you explicitly want to inspect or override context selection.

## Responsibilities
- Build a context pack with `static`, `working`, and `memory` tiers.
- Filter noisy inputs and prioritize task-relevant references.
- Add provenance for every imported reference.
- Set context TTL and refresh strategy.

## Output Contract
Return:
1. Context inventory
2. Included vs excluded references with reason
3. Context pack payload
4. TTL and refresh policy
5. Risks from missing context

## Required Rules
- Never include secrets in context payloads.
- Prefer repository-local sources over external sources.
- Mark inferred assumptions explicitly.
