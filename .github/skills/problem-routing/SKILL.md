# Problem Routing Skill

## Goal
Map a user-stated problem to the best prompt command(s), skill(s), and execution order.

## Inputs
- Problem statement
- Optional constraints (deadline, risk, environment, affected repos)

## Outputs
- Problem category
- Primary command
- Supporting commands
- Skill stack
- Execution sequence
- Clarifying question if confidence is low

## Decision Matrix
- Problem is about writing better prompts -> `prompt-coach`
- Problem is about EMSP repo ownership/routing -> `system-agent`
- Problem is full build/feature implementation -> `master-agent`
- Problem likely needs checkpoint/resume -> `session-management`
- Problem suffers from missing/noisy references -> `context-management`
- Problem likely exceeds budget/large scope -> `token-management`
- Problem requires branch/retry/stateful orchestration -> `graphify-integration`
- Problem is governance/compliance/process -> `governance-agent`

## Confidence Rule
If confidence < 0.75, ask one clarifying question before final routing.
