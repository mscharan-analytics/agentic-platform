# Agent Commands and Skills Usage

## What This Is
This is the operator guide for using slash commands and skills in this repository.

The intended workflow is linear, not circular. Start with one primary command, then move straight to execution when ready.

## How To Call Commands
In chat, call commands like this:
- `/solver-agent`
- `/worker-agent`
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

You can add a problem statement after the command, for example:
- `/solver-agent We need a new approval workflow across UI and service with minimal risk`

## Command Catalog
| Command | Use When | Output |
|---|---|---|
| `/solver-agent` | You want one front door for intake, routing, planning, and autonomous control decisions | Problem framing, execution path, risks, worker handoff |
| `/worker-agent` | You want direct implementation and verification without separate manager commands | Code changes, validation, blockers |
| `/prompt-coach` | You have a weak prompt and want it improved with teaching | Diagnosis + framework + rewrite |
| `/system-agent` | You need EMSP repo routing and boundary-safe execution | Repo map, ownership, hard-stop checks |
| `/master-agent` | You want end-to-end autonomous feature delivery | Staged plan, code, verification, audit |
| `/agent-intake` | You explicitly want a routing recommendation rather than immediate work | Primary command + internal controls |
| `/session-manager` | Advanced manual override for checkpoint/resume policy | Session plan + resume policy |
| `/context-manager` | Advanced manual override for context selection | Context pack + provenance + exclusions |
| `/token-manager` | Advanced manual override for token budgeting | Budget table + split strategy |
| `/graphify-agent` | Workflow has branching/retry/failure recovery | Graph node/edge execution design |
| `/governance-agent` | You need compliance checks for prompts/skills/workflows | Compliance matrix + remediation |
| `/problem-router` | You only know the problem, not which command to use | Recommended command stack |
| `/session-closeout` | End of chat/session and want carry-forward context saved | Persistent concise summary written |
| `/next-session-start` | Start new chat with carry-forward context already loaded | Ready-to-paste startup prompt |

## Skills Catalog
| Skill | Path | Purpose |
|---|---|---|
| session-management | `.github/skills/session-management/SKILL.md` | Run lifecycle, checkpoint, resume |
| context-management | `.github/skills/context-management/SKILL.md` | Context quality and relevance control |
| token-management | `.github/skills/token-management/SKILL.md` | Budgeting and split-session controls |
| graphify-integration | `.github/skills/graphify-integration/SKILL.md` | Graph orchestration for branching flows |
| problem-routing | `.github/skills/problem-routing/SKILL.md` | Problem-to-command mapping |

## Problem -> What To Use
Use this quick matrix when someone describes a problem.

| Problem Pattern | Primary | Supporting |
|---|---|---|
| "I want the agent to decide what to do" | `/solver-agent` | `/worker-agent` only if execution starts |
| "Implement this change now" | `/worker-agent` | `/solver-agent` if scope is unclear |
| "My prompt quality is bad" | `/prompt-coach` | `/solver-agent` if it becomes a repo task |
| "Which EMSP repo should this change go to?" | `/solver-agent` | `/system-agent` when repo rules must be enforced explicitly |
| "Build this feature end-to-end" | `/solver-agent` | `/worker-agent` |
| "This is long and may fail halfway" | `/solver-agent` | internal checkpointing; `/graphify-agent` only as manual override |
| "I don't trust the context quality" | `/solver-agent` | `/context-manager` only as manual override |
| "This will exceed context/token budget" | `/solver-agent` | `/token-manager` only as manual override |
| "Need retry, branch, and rollback paths" | `/solver-agent` | `/graphify-agent` only as manual override |
| "Are we compliant with our governance rules?" | `/solver-agent` | `/governance-agent` if a dedicated compliance readout is needed |
| "Not sure where to start" | `/solver-agent` | none |

## Recommended Execution Order (Default)
When uncertain, use this sequence:
1. `/solver-agent`
2. `/worker-agent` when execution is ready
3. Use manager commands only for explicit manual override

Avoid command loops. Do not route through intake, router, and manager prompts repeatedly.

## Practical Examples
### Example 1: Cross-repo enhancement
Input:
- "Add approval analytics card in UI and service"

Use:
1. `/solver-agent ...`
2. `/worker-agent ...`

### Example 2: Very large request
Input:
- "Create enterprise multi-tenant campaign orchestration platform"

Use:
1. `/solver-agent ...`
2. `/worker-agent ...`

### Example 3: Governance hardening
Input:
- "Validate prompts, skills, and CI governance"

Use:
1. `/solver-agent ...`
2. `/governance-agent ...` if a dedicated compliance readout is still needed

## Where Governance Is Defined
- `.github/GOVERNANCE-RULES.md`
- `.github/workflows/prompt-governance-check.yml`
- `MASTER_AGENT.md`
