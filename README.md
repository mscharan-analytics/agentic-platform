# Enterprise Agent Platform

**Python-first autonomous multi-agent system for enterprises.** Build autonomous workflows with 12 specialized agents, local-first model inference (Ollama), and enterprise-grade controls (RBAC, audit, policy enforcement).

## 🚀 Quick Start (Choose One)

### Option 1: pip install (Recommended)
```bash
pip install enterprise-agent-platform
agent-platform --goal "Implement feature X safely"
```

### Option 2: Docker (No Python needed)
```bash
docker pull enterprise-agent-platform:latest
docker run enterprise-agent-platform --goal "Your objective"
```

### Option 3: From source (Development)
```bash
git clone https://github.com/yourorg/enterprise-agent-platform.git
cd enterprise-agent-platform
pip install -e .
agent-platform --goal "Your objective"
```

## 📋 What's Included

**12 Enterprise Agents:**
- **Orchestrator** — Task routing and lifecycle
- **Solver** — Problem decomposition  
- **Planner** — Dependency-aware execution plans
- **CodeWorker** — Code implementation
- **IntegrationWorker** — External integrations
- **Tooling** — Safe tool execution
- **ContextManager** — ACP context handling
- **Browser** — Web task automation
- **Evaluator** — Quality validation
- **Critic** — Risk analysis
- **Recovery** — Autonomous failure recovery

**Enterprise Features:**
- ✅ Local-first model inference (Ollama default)
- ✅ Agent Context Protocol (ACP) for handoffs
- ✅ Agent-to-Agent (A2A) protocol for delegation
- ✅ Role-based access control (RBAC)
- ✅ Immutable audit trails
- ✅ Policy-as-code enforcement
- ✅ Structured telemetry & SLI/SLO
- ✅ Lifecycle hooks for extensibility
- ✅ Browser automation under policy

## 🏗️ Architecture

```
Tier 1: Planning         Tier 2: Execution          Tier 3: Quality
┌──────────────┐         ┌──────────────┐          ┌──────────────┐
│ Orchestrator │         │   CodeWorker │          │  Evaluator   │
└──────┬───────┘         │  Integration │          │   Critic     │
       │                 │  Browser Agt │          │  Recovery    │
┌──────────────┐         │   Tooling    │          └──────────────┘
│   Solver     │         │   Context    │
└──────┬───────┘         └──────────────┘
       │
┌──────────────┐
│   Planner    │
└──────────────┘

All agents communicate via ACP and A2A protocols
```

## 📦 Installation Details

### Requirements
- Python 3.11+
- Optional: Docker (for containerized deployment)
- Optional: Ollama (for local inference; auto-starts in Docker)

### Dependency Footprint
- **Core**: pydantic, typing-extensions (< 50 KB)
- **Optional MCP**: fastmcp (for Model Context Protocol)
- **Optional Docker**: docker (for container management)

## 💻 Local Usage Example

```bash
# Install
pip install enterprise-agent-platform

# Create goal objective
cat > my_goal.txt <<EOF
Implement a safe deployment pipeline with:
- Policy-compliant code review
- Automated testing
- Risk assessment
- Rollback automation
EOF

# Run autonomous execution
agent-platform --goal "$(cat my_goal.txt)"

# Output includes:
# - Full execution trace
# - Policy decisions per action
# - Generated artifacts
# - Audit log
```

## 🐳 Docker Usage Example

```bash
# Start local stack with Ollama
docker-compose -f deployment/docker/docker-compose.yml up -d

# Run a goal
docker run \
  --network host \
  enterprise-agent-platform \
  --goal "Deploy service with safety checks"

# Stop
docker-compose -f deployment/docker/docker-compose.yml down
```

## 🔧 Configuration

### Environment Variables
```bash
export OLLAMA_BASE_URL=http://localhost:11434  # Default
export LOG_LEVEL=INFO                          # DEBUG, INFO, WARNING
export POLICY_ENFORCE_STRICT=true              # Enforce all policies
```

### Override Model Provider (Optional)
```python
from agent_platform.model_gateway import ModelGateway, ModelProvider

gateway = ModelGateway()
# Optional: Enable cloud fallback
gateway.enable_cloud_provider(
    provider=ModelProvider.OPENAI,
    api_key="sk-..."
)
```

## 📚 Documentation

- [Architecture](docs/01-ARCHITECTURE.md) — Agent hierarchy, protocols, design
- [Quick Start](docs/02-QUICK-START.md) — Local & Docker setup
- [Project Structure](docs/03-STRUCTURE.md) — Folder layout & ownership
- [Distribution](docs/04-DISTRIBUTION.md) — Building, publishing, deployment
- [CI/CD Setup](docs/11-CICD.md) — Branching, CI, release, registry, and PyPI setup
- [End-to-End Process Diagram](docs/12-HIGH-LEVEL-ARCHITECTURE.mmd) — User-to-deployment process view
- [How To Use](docs/13-HOW-TO-USE.md) — Install, CLI usage, slash-agent usage, PR flow, and release flow

## 🧪 Development

```bash
# Clone and install dev dependencies
git clone https://github.com/yourorg/enterprise-agent-platform.git
cd enterprise-agent-platform
pip install -e .[dev]

# Run all tests
pytest -v

# Lint and type check
bash scripts/quality.sh

# Build local distribution
python -m build
```

## 📦 Publishing (For Maintainers)

```bash
# Build
python -m build

# Test locally
pip install dist/enterprise_agent_platform-*.whl

# Publish to PyPI
twine upload dist/*

# Docker
docker build -t enterprise-agent-platform:0.1.0 -f deployment/docker/Dockerfile .
docker tag enterprise-agent-platform:0.1.0 enterprise-agent-platform:latest
docker push enterprise-agent-platform:latest
```

See [Distribution Guide](docs/04-DISTRIBUTION.md) for detailed instructions.

CI runs automatically on pushes and pull requests via [ci.yml](.github/workflows/ci.yml). Releases can be triggered by pushing a `v*` tag or running [release.yml](.github/workflows/release.yml) manually after configuring the required repository secrets and variables.

## 🔐 Security & Enterprise

- **RBAC**: Built-in role-based access control
- **Audit**: Immutable execution traces + policy decisions
- **Policy-as-Code**: Define agent permissions in YAML
- **Offline-First**: Works without internet; optional cloud only
- **Secrets**: Never logged; stored in environment

## 📊 Performance

- **Startup**: ~500ms (local) or ~2s (Docker)
- **Agent execution**: ~100-500ms per step (Ollama)
- **Memory**: ~200 MB (lightweight)
- **Throughput**: 10-100 autonomous tasks/minute

## 🎯 Use Cases

✅ Autonomous code deployments with policy checks  
✅ Multi-step compliance workflows  
✅ Risk assessment & stress-testing delegated to agents  
✅ Browser-based data extraction under policy  
✅ Self-healing infrastructure via recovery agent  
✅ Enterprise workflow orchestration  

## 📄 License

Apache License 2.0 — See [LICENSE](LICENSE)

## 🤝 Contributing

PRs welcome. See [Development](#-development) section.

## ❓ FAQ

**Q: Can I use this offline?**  
A: Yes. Ollama runs locally; zero cloud dependency by default.

**Q: Do I need to write code?**  
A: No. CLI or Docker; agents execute autonomously.

**Q: How do I customize agents?**  
A: Subclass `BaseAgent` in your own `agents/my_agent/agent.py`.

**Q: How does policy enforcement work?**  
A: Every action is gated by `PolicyEngine`; RBAC rules are evaluated pre-execution.

---

**Ready to start?** → `pip install enterprise-agent-platform`
