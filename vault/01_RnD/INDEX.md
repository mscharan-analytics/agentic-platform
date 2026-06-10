# Research & Development (RnD)

## Purpose
Explore emerging agent architectures, model capabilities, integration patterns, and novel platform features. Drive innovation through experimentation, prototyping, and proof-of-concept work.

## Current State
**Status:** Foundation complete, core agents operational

### Active Components
- **Agent Framework:** Base agent architecture with hook system, policy engine, MCP integration
- **Demo Agents:** Solver, Planner, Worker, Evaluator, Scheduler agents implemented
- **MCP Integration:** Client/server setup for tool orchestration
- **Stub Implementations:** Most agent results are deterministic stubs, not yet calling ModelGateway

### Known Gaps
- ModelGateway not fully wired to production LLM endpoints
- No live model reasoning (all placeholder/deterministic flows)
- Policy engine not fully enforced at runtime
- Parallel agent coordination incomplete

## Active Decisions

### Decision: Agent Reasoning Architecture
- **Adopted:** Hook-based system with policy engine intercepts
- **Rationale:** Enables audit, control, and dynamic behavior injection
- **Status:** Implemented but not in production flow

### Decision: MCP for Tool Integration
- **Adopted:** Model Context Protocol for extensible tool chains
- **Rationale:** Standards-based, framework-agnostic, proven in market
- **Status:** Basic setup complete, needs production hardening

### Decision: Stub-First Development
- **Adopted:** Demo agents use deterministic responses initially
- **Rationale:** Enables end-to-end system testing without model costs
- **Status:** Ready to migrate to live reasoning on demand

## Owned Assets

### Code
- `/src/agent_platform/agents/` - Agent implementations
- `/src/agent_platform/mcp/` - MCP client/server
- `/src/agent_platform/orchestration/` - Hook and orchestrator systems
- `/src/agent_platform/policy/` - Policy engine (stub)

### Documentation
- `docs/09-MCP-INTEGRATION.md` - MCP architecture
- `docs/10-REPO-RUNTIME-FLOW.mmd` - Sequence diagram of execution paths

### Experiments (if any)
- None currently tracked

## Next Steps (Priority Order)
1. **Wire ModelGateway to LLM endpoints** - Enable real reasoning in worker agents
2. **Implement live policy enforcement** - Move from audit to active control
3. **Build parallel coordination system** - Support true concurrent agent execution
4. **Expand agent catalog** - Add specialized agents (recovery, validation, deployment)

## Risks & Blockers
- No current LLM endpoint configured → blocks live reasoning
- MCP validation needs formalization → before production deployment
- Policy engine needs runtime hooks → before enforcement can work

## Change Log
- **2026-04-10:** Initial vault setup during brain system initialization
