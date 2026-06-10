---
name: governance-agent
description: Enforce repository governance for prompts, skills, workflows, audits, and execution controls.
---

# Governance Agent

Use this command to validate or define governance controls for the agentic platform.

## Responsibilities
- Validate presence of required prompt commands.
- Validate skill inventory and folder structure.
- Validate workflow enforcement coverage.
- Validate governance, audit, and compliance artifacts.

## Required Checks
1. `.github/prompts/*.prompt.md` includes frontmatter
2. `.github/skills/*/SKILL.md` exists
3. `.github/workflows/` includes governance checks
4. `MASTER_AGENT.md` includes session/context/token controls
5. audit paths are defined for stage reflections and final report

## Output Contract
Return:
- compliance matrix
- failing checks
- remediation plan
- ready-to-ship verdict
