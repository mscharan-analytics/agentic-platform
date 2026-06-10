# Agent Governance Rules

## Purpose
This document defines mandatory governance for all prompts, skills, workflows, and autonomous runs in this repository.

## Core Rules
1. Every slash command prompt must live in `.github/prompts/*.prompt.md` and include YAML frontmatter with `name` and `description`.
2. Every reusable skill must live in `.github/skills/<skill-name>/SKILL.md`.
3. Every autonomous run must apply session, context, and token management.
4. Production-impacting actions require explicit verification and audit artifacts.
5. Containerization requirements in `MASTER_AGENT.md` are mandatory and cannot be bypassed.
6. Every session must end with concise context persisted to `.github/context/summaries/SESSION-LATEST.md`.

## Session Management Policy
- Each run must declare `session_id`, `run_id`, and stage checkpoints.
- Long runs must checkpoint after each stage and persist recovery state.
- Resumed sessions must load prior state before new execution.

## Context Management Policy
- Use a three-tier context model: `static` (rules), `working` (current task), `memory` (historical learnings).
- Enforce relevance filtering before injecting context into prompts.
- Include provenance metadata for external references.

## Token Management Policy
- Define token budget by stage before execution.
- Enforce hard stop or split when estimated budget is exceeded.
- Prefer tables and structured outputs over repetitive prose.

## Graph Workflow Policy
- Use graph orchestration when the plan has branching or recoverable subflows.
- Every node must define inputs, outputs, retries, and failure transition.
- Graph execution must emit trace logs suitable for audit.

## Required Slash Commands
- `/prompt-coach`
- `/system-agent`
- `/master-agent`
- `/agent-intake`
- `/session-manager`
- `/context-manager`
- `/token-manager`
- `/graphify-agent`
- `/governance-agent`
- `/problem-router`
- `/session-closeout`
- `/next-session-start`

## Stuck Clarification Policy
- If blocked by ambiguity, ask 1-4 concise verification questions.
- Questions must be multiple-choice where possible.
- Do not ask follow-ups when confidence is high and risk is low.

## CI Enforcement
Governance workflows under `.github/workflows/` must validate:
- prompt frontmatter
- required command files
- required skill files
- no empty governance artifacts
