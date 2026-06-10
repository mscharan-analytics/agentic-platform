# Product

## Purpose
Define product vision, user-facing features, roadmap, requirements, and constraints. Align platform capabilities with user needs and market positioning.

## Current State
**Status:** MVP phase - core orchestration system ready for early adopters

### Product Definition
- **Platform Name:** Enterprise Agent Platform (EAP)
- **Primary Use Case:** Multi-agent orchestration for enterprise modernization and software delivery tasks
- **Target User:** Enterprise DevOps teams, platform engineers, software architects
- **Current Stage:** Foundation complete, early deployment phase

### Feature Set (MVP)
- Agent orchestration with policy engine
- Problem decomposition (Solver agent)
- Execution planning (Planner agent)
- Code generation and execution (Worker agents)
- Results evaluation (Evaluator agent)
- Extensible via MCP tool integration

### Known Limitations
- Single-session execution model (no true persistence yet)
- Deterministic agent responses (no live LLM reasoning)
- Limited integration points (stub adapters for Azure DevOps, GitHub, Jenkins, etc.)
- No production deployment model yet

## Active Decisions

### Decision: Target Persona
- **Adopted:** Platform engineers and DevOps architects
- **Rationale:** Can understand agent orchestration; can configure policies; can integrate via MCP
- **Status:** Locked for MVP

### Decision: MVP Scope
- **Adopted:** Local execution only; self-hosted runners; no SaaS model for v1
- **Rationale:** Reduces operational complexity; maintains customer data privacy; simplifies deployment
- **Status:** Implementation complete, deployment docs in progress

### Decision: Extensibility
- **Adopted:** MCP for tool integration, Python for extensions
- **Rationale:** Standards-based, proven ecosystem, easy for platform engineers
- **Status:** Foundation ready

## Owned Assets

### Code
- `/src/agent_platform/main.py` - Platform entry point
- `/src/agent_platform/agents/` - Agent implementations
- `/src/agent_platform/contracts/` - A2A and ACP protocol definitions
- Deployment adapters

### Documentation
- `docs/02-QUICK-START.md` - Getting started
- `docs/13-HOW-TO-USE.md` - Feature overview
- `docs/04-DISTRIBUTION.md` - Deployment models

### Requirements & Roadmap
- None formalized yet - should be added to vault

## Roadmap (Planned Phases)
1. **Phase 1 (Now):** MVP - self-hosted, demo agents, deterministic flows
2. **Phase 2 (Q3 2026):** Live reasoning via LLM endpoints, production policy enforcement
3. **Phase 3 (Q4 2026):** Multi-agent parallel execution, advanced scheduling
4. **Phase 4 (2027):** SaaS deployment model, marketplace for agent templates

## Risks & Blockers
- No formal requirements document → ambiguous MVP definition
- Production deployment workflow incomplete → blocks early customer pilots
- Integration adapters are stubs → limited real-world utility

## Change Log
- **2026-04-10:** Initial product definition in vault setup
