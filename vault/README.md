# Persistent Project Brain System

## Overview

The Persistent Project Brain System is an operational control system that enables long-running, multi-session work across humans and AI agents. It replaces conversation-based context switching with an explicit, inspectable, written record of project state.

**This is not a note-taking system.** This is an operational control system for building software and products.

### Core Design Principles

1. **The project, not the agent, is the source of memory**
   - All critical context lives in the vault
   - No hidden state in agent memory
   - Any agent can resume any work

2. **All decisions must be explicit, inspectable, and written**
   - Write it or it doesn't exist
   - Every department maintains an INDEX.md with decisions
   - Decisions are dated and justified

3. **Execution is driven by dependency graphs, not conversations**
   - Tasks have explicit dependencies (other task IDs)
   - Unblocked tasks can be assigned in parallel
   - Status is tracked in EXECUTION_PLAN.md

4. **Any session must be resumable with zero prior context**
   - Read the execution plan → know what needs doing
   - Read the latest handoff note → know what just happened
   - Read department indexes → know the context
   - Start work

---

## System Architecture

### 1. The Vault

The vault is the project's persistent memory. Location: `vault/`

```
vault/
├── 01_RnD/
│   ├── INDEX.md              # Research & Development department
│   └── *.md                  # RnD artifacts, experiments
├── 02_Product/
│   ├── INDEX.md              # Product definition & roadmap
│   └── *.md                  # Product docs
├── 03_Marketing/
│   ├── INDEX.md              # Marketing & positioning
│   └── *.md                  # Market analysis, messaging
├── 04_Community/
│   ├── INDEX.md              # Developer experience
│   └── *.md                  # Community docs
├── 05_Legal/
│   ├── INDEX.md              # Compliance & legal
│   └── *.md                  # Policies, templates
├── 06_Operations/
│   ├── INDEX.md              # Deployment & infrastructure
│   └── *.md                  # Runbooks, guides
├── 07_Security/
│   ├── INDEX.md              # Security & threat models
│   └── *.md                  # Security policies
├── 08_Docs/
│   ├── INDEX.md              # Documentation governance
│   └── *.md                  # Doc planning
├── EXECUTION_PLAN.md         # Master dependency graph
├── HANDOFF_NOTES.md          # Session wrap-up trail
└── scripts/
    ├── resume.sh             # Session startup
    └── wrap-up.sh            # Session conclusion
```

### 2. Department Indexes

Each department folder contains an `INDEX.md` that defines:

| Section | Purpose |
|---------|---------|
| Purpose | Why this department exists |
| Current State | Status, active components, known gaps |
| Active Decisions | Important choices made (and rationale) |
| Owned Assets | Files, processes, responsibilities |
| Risks & Blockers | What's preventing progress |
| Next Steps | Priorities for this department |

**Example:** [vault/02_Product/INDEX.md](02_Product/INDEX.md)

### 3. Execution Plan

The **EXECUTION_PLAN.md** is the master document that governs all work.

| Column | Meaning |
|--------|---------|
| Task ID | Unique identifier (TASK.XXXX) |
| Title | What work is this? |
| Owner | Human or agent responsible |
| Status | 🔲 Unblocked, 🔄 In Progress, ✅ Done, 🔴 Blocked |
| Dependencies | List of task IDs that must complete first |
| Effort | Estimated hours |
| Output | Files, artifacts, decisions produced |

Tasks are organized by **phase** (Foundation, Ready-for-Pilot, Production, Future) and by **theme** (Platform Hardening, Documentation, Security, etc.).

**Rule:** Tasks become unblocked **only when all dependencies complete**.

### 4. Handoff Notes

When a session ends, a handoff note is appended to `HANDOFF_NOTES.md`.

Each handoff note contains:

- What work was completed
- What files/decisions changed
- What tasks are now unblocked
- Known risks or open questions
- Session metadata (when, who, where)

**Purpose:** Enable the next agent/human to resume with zero context loss.

---

## How to Start a Session

### 1. Run Resume Script

```bash
./vault/scripts/resume.sh
```

This script:
- Reads the execution plan
- Lists all unblocked tasks
- Shows the most recent handoff note
- Displays department status
- Recommends next steps

### 2. Read the Execution Plan

Open `vault/EXECUTION_PLAN.md` to understand:
- What phase the project is in
- What tasks are ready to start
- What's blocking other work
- Who owns what

### 3. Pick a Task

Choose the highest-leverage unblocked task. Criteria:
- Unblocks other critical work
- Aligned with current phase
- Has clear success criteria
- Owner (agent or human) is available

### 4. Read Department Indexes

Before starting work, read the relevant department INDEX.md to understand:
- Current state and active decisions
- Owned assets you'll be modifying
- Constraints and dependencies
- Known risks

### 5. Execute Work

Do the work. Update files, make decisions, create artifacts.

Store all non-trivial artifacts in the vault:
- Strategic decisions → department INDEX
- New assets → department folder
- Handoff notes → append to HANDOFF_NOTES.md

### 6. Wrap-Up

When your session is ending, run:

```bash
./vault/scripts/wrap-up.sh
```

This script:
1. Prompts you for a session summary (what you completed)
2. Asks what changed and what's now unblocked
3. Creates a handoff note
4. Updates and commits vault changes to git
5. Leaves everything ready for the next session

---

## Parallel Execution Model

Multiple agents can work simultaneously on **unblocked tasks**.

### Requirements

- Each agent works in isolation (separate branch, worktree, or container)
- All outputs flow back to the vault
- Conflicts are resolved explicitly via written decisions

### Example: Two Agents in Parallel

```
Agent 1 (RnD): Working on TASK.1003 (ModelGateway integration)
  └─ Branch: feat/modelgateway
  └─ Output: /src/agent_platform/model_gateway/

Agent 2 (Security): Working on TASK.1007 (Threat model)
  └─ Branch: feat/threat-model
  └─ Output: vault/07_Security/THREAT_MODEL.md

When both complete:
  - Each creates a PR
  - Updates EXECUTION_PLAN.md to mark tasks ✅ Done
  - Merges to main
  - Next agent resumes with BOTH tasks unblocked
```

### Conflict Resolution

If two agents modify the same file (e.g., EXECUTION_PLAN.md):

1. **Explicit merge:** Write a decision document explaining the resolution
2. **Replay conflicts:** One agent re-runs their edits on top of the merged state
3. **Coordinator:** Designate a human to arbitrate conflicts

---

## Key Operations

### Check Project Status

```bash
cat vault/EXECUTION_PLAN.md          # What needs doing?
tail -50 vault/HANDOFF_NOTES.md      # What just happened?
cat vault/0X_Department/INDEX.md     # What's this department doing?
```

### Mark a Task In-Progress

Edit `vault/EXECUTION_PLAN.md`:
- Change task status from 🔲 (unblocked) to 🔄 (in-progress)
- Add your name or agent ID as the owner

### Mark a Task Done

Edit `vault/EXECUTION_PLAN.md`:
1. Change status to ✅ Done
2. Record the output files/artifacts
3. Check for dependent tasks that are now unblocked
4. Change dependent task status to 🔲 if all dependencies met

### Add a New Task

If you discover work that wasn't planned:
1. Create a new task ID (next sequential TASK.XXXX)
2. Add it to the appropriate phase in EXECUTION_PLAN.md
3. Set dependencies (what must finish first?)
4. Set status to 🔲 (unblocked) or 🔴 (blocked)
5. Add to relevant department's owned assets

### Update a Department Index

When a department's state changes materially:
1. Edit `vault/0X_Department/INDEX.md`
2. Update "Current State" section
3. Update "Active Decisions" if decisions changed
4. Move completed items to "Change Log"
5. Commit to git

---

## Rules & Policies

### Rule 1: No Hidden State
- If it's not written in the vault, it doesn't exist
- "I'll remember to tell the next agent" is not acceptable
- Create placeholders if you don't have answers yet

### Rule 2: Explicit Dependencies
- Every task must list what it depends on
- Create blocking tasks if dependencies don't exist
- Circular dependencies are an error; escalate

### Rule 3: Asynchronous-First
- Assume the next agent is 3 days away
- Write everything they need to understand your work
- No verbal handoffs, no "I'll explain it to you"

### Rule 4: Write Before You Talk
- Document decisions **before** seeking approval
- Make a proposal in writing
- Get feedback in writing
- Record the final decision in the vault

### Rule 5: Immutable History
- Never delete handoff notes
- Never rewrite history in EXECUTION_PLAN.md
- Corrections are new entries with dates and reasoning

---

## Success Criteria

The system is working if:

- ✅ A fresh agent can resume work mid-project with no prior context
- ✅ Multiple agents can work in parallel without coordination overhead
- ✅ Project state survives tool changes, model swaps, and agent restarts
- ✅ The vault tells a complete, auditable story of how the project evolved
- ✅ All critical decisions are written and justified
- ✅ Handoff notes enable seamless continuation

---

## Troubleshooting

### "I don't know where to start"
1. Run `./vault/scripts/resume.sh`
2. Look for 🔲 (unblocked) tasks in EXECUTION_PLAN.md
3. Read the relevant department INDEX
4. Pick the highest-leverage task

### "A task I need is blocked"
1. Check what it depends on in EXECUTION_PLAN.md
2. Is that dependency listed? If not, update it
3. Can you unblock it? Create a parallel sub-task
4. If truly blocked, add a note in the task and move on

### "I'm not sure if my decision is right"
1. Write the decision in the relevant department INDEX
2. Explain the rationale and alternatives
3. Leave it for review/feedback
4. Record the feedback and final decision

### "Multiple agents changed the same file"
1. Merge conflicts are expected in git
2. Resolve manually (usual git workflow)
3. If the conflict is in EXECUTION_PLAN.md, ensure task statuses are consistent
4. Add a note explaining the conflict resolution

---

## Session Checklist

### Start of Session ✅
- [ ] Run `./vault/scripts/resume.sh`
- [ ] Read EXECUTION_PLAN.md for current phase and unblocked tasks
- [ ] Read most recent HANDOFF_NOTES.md entry
- [ ] Read relevant department INDEX.md
- [ ] State your assumptions and next steps (to user or log)
- [ ] Mark chosen task as 🔄 in-progress

### During Session ✅
- [ ] Update vault files as you work
- [ ] Make decisions explicit (write them down)
- [ ] Track new risks or blockers
- [ ] Don't rely on prior context beyond vault

### End of Session ✅
- [ ] Update task status in EXECUTION_PLAN.md
- [ ] Mark newly unblocked tasks
- [ ] Create/update department INDEX if changed
- [ ] Run `./vault/scripts/wrap-up.sh`
- [ ] Review handoff note for completeness
- [ ] Commit and push

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-04-10 | Initial brain system established |

---

## Questions?

If something is unclear:
1. Check the department INDEX that owns it
2. Search HANDOFF_NOTES.md for prior context
3. Create a placeholder document flagged as [TODO]
4. Leave it for the next session to resolve

**Remember:** The vault is the source of truth. Keep it current, keep it clear, keep it complete.
