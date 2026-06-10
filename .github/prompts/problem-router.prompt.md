---
name: problem-router
description: Describe a problem and get a recommendation for solver-agent or worker-agent, with helper controls applied internally.
---

# Problem Router

Use this when a user describes a problem and needs guidance on which command or skill to run first.

## Input
- Problem statement in plain English
- Optional constraints: time, risk, repo scope, production impact

## Output Contract
Return exactly these sections:
1. Problem Classification
2. Recommended Primary Command
3. Why This Command
4. Internal Controls To Apply
5. Execution Order
6. Risk Notes
7. If Unclear, Clarifying Question

## Routing Rules
- Architecture, intake, repo analysis, planning, ambiguity resolution -> `/solver-agent`
- Clear implementation, code changes, tests, validation -> `/worker-agent`
- Repo ownership / EMSP boundary -> `/solver-agent` with system rules applied
- Long scope, missing context, or token risk -> keep `/solver-agent` or `/worker-agent` as primary and apply helper controls internally
- Governance/compliance uncertainty -> `/solver-agent` with governance notes
- Never output circular routing like solver -> router -> intake -> manager -> solver.
- Return one primary command and only one optional follow-on step when necessary.

## Example
Problem: "We need to add a new CCB feature, not sure which repos are impacted, and this might be a long run."

Recommended:
- Primary: `/solver-agent`
- Internal controls: context-management, session-management, token-management
- Follow-on: `/worker-agent` after scope is resolved
