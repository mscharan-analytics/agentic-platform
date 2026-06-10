# Architecture

## Folder Structure

```
enterprise-agent-platform/
├── src/agent_platform/
│   ├── agents/                          # 12 enterprise agent types
│   │   ├── orchestrator/                # Task routing and lifecycle
│   │   ├── solver/                      # Problem decomposition
│   │   ├── planner/                     # Dependency-aware planning
│   │   ├── workers/                     # Code and integration workers
│   │   ├── evaluator/                   # Quality validation
│   │   ├── critic/                      # Risk analysis
│   │   ├── tooling/                     # Tool execution (normalized)
│   │   ├── context_manager/             # ACP context management
│   │   ├── browser/                     # Policy-gated browser tasks
│   │   └── recovery/                    # Autonomous recovery
│   │   ├── validation/                  # Go/No-Go validation gate
│   │   ├── scheduler/                   # Build/test/release timing orchestration
│   │   └── deployment/                  # CI/CD environment progression
│   ├── contracts/                       # Protocol definitions
│   │   ├── acp.py                       # Agent Context Protocol
│   │   └── a2a.py                       # Agent-to-Agent protocol
│   ├── orchestration/                   # Execution engine
│   │   ├── orchestrator.py              # Autonomous runner loop
│   │   └── hooks.py                     # Lifecycle hooks & audit
│   ├── policy/                          # Policy enforcement
│   ├── model_gateway/                   # Ollama-first, cloud-optional
│   ├── security/                        # RBAC, audit trails
│   ├── telemetry/                       # Metrics, SLI/SLO
│   ├── integrations/                    # Jira/Figma/Lucid requirements intake adapters
│   ├── validation/                      # Static analysis execution adapters
│   ├── deployment_adapters/             # GitHub Actions/Azure DevOps/Jenkins dispatch
│   └── mcp/                             # FastMCP server
├── tests/                               # Unit, integration, e2e
├── deployment/docker/                   # Dockerfile, docker-compose
├── scripts/                             # bootstrap, test, quality.sh
└── docs/                                # Architecture, guides
```

## Agent Hierarchy

15 agents organized into 4 tiers:

### Tier 1: Planning & Strategy
- **Orchestrator**: Routes tasks, manages lifecycle
- **Solver**: Decomposes objectives
- **Planner**: Creates dependency DAGs

### Tier 2: Execution & Assurance
- **CodeWorker**: Implements code changes
- **IntegrationWorker**: Validates integrations
- **Tooling**: Executes tool calls (normalized)
- **ContextAgent**: Manages ACP context
- **BrowserAgent**: Policy-gated web tasks

### Tier 3: Validation & Release Control
- **ValidationAgent**: Test/static/policy go-no-go gate
- **SchedulerAgent**: Pipeline timing and trigger orchestration
- **DeploymentAgent**: Environment-aware deployment transitions

### Tier 4: Quality & Safety
- **Evaluator**: Validates against criteria
- **Critic**: Stress-tests and risk-analyzes
- **RecoveryAgent**: Autonomous failure recovery

## SDLC Loop Coverage

The platform now supports a repeatable SDLC loop in `AutonomousRunner.run_sdlc_pipeline`:
1. Requirements intake (Figma/Lucid/Jira sources declared in metadata)
2. Task conversion (stories -> executable tasks)
3. Code generation (+ test/config production)
4. Build/package
5. Validation gate (Go/No-Go)
6. Pass/fail handling (rework loop on fail)
7. Deployment across envs (dev/staging/prod)
8. Observability checkpoint (health/logs/metrics summary)

This aligns to your target design where validation and scheduler orchestration run as first-class capabilities.

## External Integration Runtime

The intake/deployment adapters are API-first and environment-driven:

- Jira: `JIRA_BASE_URL`, `JIRA_PROJECT_KEY`, `JIRA_API_TOKEN`
- Figma: `FIGMA_API_TOKEN`, optional `FIGMA_FILE_KEY`
- Lucid: `LUCID_API_TOKEN`, optional `LUCID_DOC_ID`
- GitHub Actions: `GITHUB_REPOSITORY`, `GITHUB_TOKEN`, optional `GITHUB_API_BASE`
- Azure DevOps: `AZDO_ORG_URL`, `AZDO_PROJECT`, `AZDO_PIPELINE_ID`, `AZDO_PAT`
- Jenkins: `JENKINS_URL`, `JENKINS_USER`, `JENKINS_API_TOKEN`, optional `JENKINS_JOB`

If required credentials/config are missing, adapters fall back to deterministic simulated responses so orchestration can continue in local/dev mode.

## Core Protocols

### Agent Context Protocol (ACP)
Versioned context envelope for agent handoff:
- Integrity hash (sha256)
- Provenance metadata
- TTL and expiry
- Classification levels

### Agent-to-Agent (A2A) Protocol
Reliable inter-agent messaging:
- Message types: request, delegate, result, fail, cancel
- At-least-once delivery semantics
- Auth context and policy gates
- State machine with 9 states

## Local-First Model Strategy

### Default: Ollama
- Runs on developer laptop
- No cloud dependency
- Fast local inference

### Optional: Cloud Fallback
- OpenAI, Claude, others via adapter
- Enabled only by explicit policy
- Transparent fallback if Ollama unavailable

### Offline Mode
- Deterministic mocked responses
- Full test coverage without network
- Reproducible test runs
