# Project Structure

```
enterprise-agent-platform/
├── README.md                        # Project overview
├── pyproject.toml                   # Python project config
│
├── src/agent_platform/
│   ├── __init__.py
│   ├── main.py                      # CLI entrypoint
│   ├── contracts/                   # Shared protocols
│   │   ├── __init__.py
│   │   ├── acp.py                   # Agent Context Protocol
│   │   └── a2a.py                   # Agent-to-Agent Protocol
│   ├── agents/                      # All 12 agent types
│   │   ├── base.py                  # BaseAgent class
│   │   ├── catalog.py               # Agent registry
│   │   ├── orchestrator/
│   │   │   ├── __init__.py
│   │   │   └── agent.py             # OrchestratorAgent
│   │   ├── solver/
│   │   │   ├── __init__.py
│   │   │   └── agent.py             # SolverAgent
│   │   ├── planner/
│   │   │   ├── __init__.py
│   │   │   └── agent.py             # PlannerAgent
│   │   ├── workers/
│   │   │   ├── __init__.py
│   │   │   ├── code_worker.py       # CodeWorker
│   │   │   └── integration_worker.py # IntegrationWorker
│   │   ├── evaluator/
│   │   │   ├── __init__.py
│   │   │   └── agent.py             # EvaluatorAgent
│   │   ├── critic/
│   │   │   ├── __init__.py
│   │   │   └── agent.py             # CriticAgent
│   │   ├── tooling/
│   │   │   ├── __init__.py
│   │   │   └── agent.py             # ToolingAgent
│   │   ├── context_manager/
│   │   │   ├── __init__.py
│   │   │   └── agent.py             # ContextAgent
│   │   ├── browser/
│   │   │   ├── __init__.py
│   │   │   └── agent.py             # BrowserAgent
│   │   └── recovery/
│   │       ├── __init__.py
│   │       └── agent.py             # RecoveryAgent
│   ├── orchestration/               # Execution engine
│   │   ├── __init__.py
│   │   ├── orchestrator.py          # AutonomousRunner
│   │   └── hooks.py                 # Lifecycle hooks
│   ├── policy/
│   │   └── engine.py                # PolicyEngine
│   ├── model_gateway/
│   │   └── __init__.py              # Ollama + cloud adapters
│   ├── security/
│   │   └── __init__.py              # RBAC, audit
│   ├── telemetry/
│   │   └── __init__.py              # Metrics & SLI/SLO
│   └── mcp/
│       └── server.py                # FastMCP server
│
├── tests/
│   ├── test_contracts.py            # Protocol tests
│   └── test_orchestrator.py         # Runner tests
│
├── deployment/docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── scripts/
│   ├── bootstrap.sh                 # Environment setup
│   ├── test.sh                      # Run tests
│   └── quality.sh                   # Lint & type checks
│
└── docs/
    ├── 01-ARCHITECTURE.md
    ├── 02-QUICK-START.md
    └── 03-STRUCTURE.md
```

## Key Principles

1. **Clear Hierarchy**: Each agent owns one folder; responsibilities are explicit.
2. **Protocol-First**: ACP and A2A are shared contracts; enforcement is central.
3. **Autonomous by Default**: Execution loop runs until completion or hard stop.
4. **Local-First**: Ollama is default model backend; cloud is optional.
5. **Enterprise-Ready**: RBAC, audit, telemetry, hooks built-in from start.
