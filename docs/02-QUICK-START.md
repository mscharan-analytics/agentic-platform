# Quick Start Guide

## Local Development (Single Laptop)

### 1. Bootstrap Environment
```bash
cd enterprise-agent-platform
bash scripts/bootstrap.sh
```

### 2. Activate Virtual Environment
```bash
source .venv/bin/activate
```

### 3. Run Your First Autonomous Execution
```bash
agent-platform --goal "Implement feature X with safety checks"
```

### 4. Run Tests
```bash
bash scripts/test.sh
```

## Docker Deployment (Local or Server)

### 1. Build and Start Local Stack
```bash
docker-compose -f deployment/docker/docker-compose.yml up -d
```

### 2. Check Status
```bash
docker-compose -f deployment/docker/docker-compose.yml logs agent-platform
```

### 3. Stop Stack
```bash
docker-compose -f deployment/docker/docker-compose.yml down
```

## Multi-Laptop Setup

### On New Laptop:
1. Clone repo
2. Run: `bash scripts/bootstrap.sh`
3. Create `.env` with secrets (if production RBAC enabled)
4. Run: `agent-platform --goal "Your objective"`

Or use Docker to avoid local Python setup entirely.

## Project Dependencies

Core:
- `pydantic>=2.7.0` — schema validation
- `typing-extensions>=4.9.0` — type hints

Dev:
- `pytest>=8.0.0` — testing
- `pytest-asyncio>=0.23.0` — async tests
- `ruff>=0.5.0` — linting
- `mypy>=1.10.0` — type checking

Optional:
- `fastmcp>=0.2.0` — MCP server runtime

## Folder Permissions & Hierarchy

Each agent has its own folder under `agents/`:
- `agents/orchestrator/` — Owns routing, dispatch
- `agents/solver/` — Owns problem analysis
- `agents/planner/` — Owns task DAG creation
- `agents/workers/` — Owns execution
- `agents/evaluator/` — Owns validation
- etc.

Supporting systems live in top-level modules:
- `model_gateway/` — Model routing (Ollama-first)
- `security/` — RBAC and audit
- `telemetry/` — Metrics and observability
- `policy/` — Policy enforcement
- `contracts/` — Shared protocol definitions
