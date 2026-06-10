# Developer Onboarding Guide (Copy-Paste Ready)

> **You asked:** "How do we get this to work for developers without loading all these files?"
>
> **Answer:** We've built it so developers never see the source tree. They get a 27 KB wheel or a Docker container. That's it.

---

## 📊 How It All Flows

```
Your Enterprise
    ↓
    You publish one of:
    ├── dist/enterprise_agent_platform-0.1.0-py3-none-any.whl (to PyPI or internal)
    ├── Docker image (to registry)
    └── GitHub release tag (auto-builds both above)
    ↓
Developers' Laptops (no cloning needed)
    ├── Option A: pip install enterprise-agent-platform
    ├── Option B: docker pull enterprise-agent-platform
    └── Option C: pip install https://internal.company.com/wheel.whl
    ↓
Developers immediately:
    $ agent-platform --goal "Your objective"
    (complete autonomous execution)
    ↓
That's it! ✅
```

---

## 🎯 What Developers See vs. Don't See

### What Developers DO See
```bash
$ pip install enterprise-agent-platform
Collecting enterprise-agent-platform
  Downloading enterprise_agent_platform-0.1.0-py3-none-any.whl (27 kB)
Installing collected packages: enterprise-agent-platform, pydantic
Successfully installed enterprise-agent-platform-0.1.0

$ agent-platform --goal "Deploy safely"
[autonomous execution output]

trace_id: a1b2c3d4...
solver: ✓ Decomposed
planner: ✓ Created DAG
steps: 3
evaluation: ✓ PASS
```

### What Developers DON'T See
```
src/
  agent_platform/
    agents/          ← Hidden behind wheel
    contracts/       ← Hidden behind wheel
    orchestration/   ← Hidden behind wheel
    policies/        ← Hidden behind wheel
    ... (all implementation details)

Only 27 KB gets installed!
```

---

## 👨‍💻 Three Developer Personas - Three Paths

### Persona 1: "Just Use It" Developer
```
Goal: Run autonomous workflows on my laptop
Time: 10 seconds
Path:
  $ pip install enterprise-agent-platform
  $ agent-platform --goal "Deploy with checks"
  Done ✅
```

### Persona 2: "Containerized" DevOps Engineer
```
Goal: Run in Docker, no local Python
Time: 30 seconds
Path:
  $ docker pull myregistry.com/enterprise-agent-platform:latest
  $ docker run -it myregistry.com/enterprise-agent-platform \
      --goal "Your objective"
  Done ✅
```

### Persona 3: "Custom Agents" Contributor
```
Goal: Extend with custom agents
Time: 2 minutes (includes clone)
Path:
  $ git clone https://github.com/yourorg/enterprise-agent-platform
  $ cd enterprise-agent-platform
  $ pip install -e .[dev]
  $ # Edit src/agent_platform/agents/my_custom/agent.py
  $ pytest
  $ pip install -e .  (reinstall in dev mode)
  $ agent-platform --goal "Test custom agent"
  Done ✅
```

---

## 🚀 Publishing (You Do Once Per Release)

### For PyPI (Public)

```bash
# 1. Test locally
pip install -e .[dev]
pytest
bash scripts/quality.sh

# 2. Build
python -m build

# 3. Publish (auto via GitHub Actions OR manual)
twine upload dist/*

# 4. Developers immediately can:
pip install --upgrade enterprise-agent-platform
```

### For Docker (Private Registry)

```bash
# 1. Build image
docker build -f deployment/docker/Dockerfile \
  -t myregistry.com/enterprise-agent-platform:0.1.0 .

# 2. Tag latest
docker tag myregistry.com/enterprise-agent-platform:0.1.0 \
  myregistry.com/enterprise-agent-platform:latest

# 3. Push
docker push myregistry.com/enterprise-agent-platform:latest

# 4. Developers immediately can:
docker pull myregistry.com/enterprise-agent-platform:latest
docker run myregistry.com/enterprise-agent-platform --goal "..."
```

### For GitHub Releases

```bash
# 1. Tag a release
git tag v0.1.0
git push origin v0.1.0

# 2. GitHub Actions auto:
#    - Builds wheel + sdist
#    - Builds Docker image
#    - Publishes to PyPI (if token configured)
#    - Pushes image to registry (if credentials configured)
#    - Creates GitHub Release with artifacts

# 3. Developers see release on GitHub, can:
# - Download .whl directly
# - Use specific Docker tag
# - Or just: pip install --upgrade (if on PyPI)
```

---

## 📋 What Gets Distributed (In Charts)

### pip Wheel Contents (27 KB)
```
enterprise_agent_platform-0.1.0-py3-none-any.whl
├── agent_platform/
│   ├── agents/
│   │   ├── orchestrator/agent.py
│   │   ├── solver/agent.py
│   │   ├── planner/agent.py
│   │   ├── workers/ (code + integration)
│   │   ├── evaluator/agent.py
│   │   ├── critic/agent.py
│   │   ├── browser/agent.py
│   │   ├── tooling/agent.py
│   │   ├── context_manager/agent.py
│   │   └── recovery/agent.py
│   ├── contracts/ (ACP, A2A)
│   ├── orchestration/ (runner, hooks)
│   ├── policy/ (RBAC engine)
│   ├── model_gateway/ (Ollama routing)
│   ├── security/ (audit, RBAC)
│   ├── telemetry/ (metrics)
│   ├── mcp/ (FastMCP server)
│   └── main.py (CLI entry)
├── entry_points.txt  (agent-platform command)
└── dist-info/
```

### Docker Image Contents (~150 MB)
```
enterprise-agent-platform:latest
├── FROM python:3.11-slim
├── + apt deps (curl, ca-certificates)
├── + pip packages (pydantic, etc.)
├── + Extracted wheel (27 KB)
├── + Entrypoint: agent-platform
├── + Healthcheck
└── READY TO RUN
```

---

## 📚 Developer Docs They'll See

After `pip install`, developers can read:
```bash
$ pip show enterprise-agent-platform
Name: enterprise-agent-platform
Version: 0.1.0
Home-page: https://github.com/yourorg/enterprise-agent-platform
Summary: Enterprise autonomous multi-agent platform

$ python -c "from agent_platform import *; help(agent_platform)"
[Shows docstrings from installed package]
```

Docs location:
```bash
# All in your repo, available on GitHub/internal docs site
docs/
├── 01-ARCHITECTURE.md
├── 02-QUICK-START.md
├── 03-STRUCTURE.md
├── 04-DISTRIBUTION.md
└── 05-DISTRIBUTION-MODELS.md
```

---

## 🔧 Configuration for Developers

After install, developers can configure with environment variables:
```bash
export OLLAMA_BASE_URL=http://localhost:11434
export LOG_LEVEL=DEBUG
export POLICY_ENFORCE_STRICT=true
export PYTHONUNBUFFERED=1

agent-platform --goal "Your objective"
```

Or Python SDK:
```python
from agent_platform.model_gateway import ModelGateway, ModelProvider

gateway = ModelGateway()
gateway.enable_cloud_provider(ModelProvider.OPENAI, "sk-...")
```

---

## ❓ Common Questions Developers Ask

**Q: Will the wheel work on my Mac/Linux/Windows?**  
A: Yes. `py3-none-any` means Python 3 only (no C extensions), universal.

**Q: How big is it to download?**  
A: 27 KB. Plus pydantic (~5 MB). Tiny.

**Q: Can I use it offline after install?**  
A: Yes. Ollama runs locally; zero cloud dependency.

**Q: What if I want to customize?**  
A: Clone source, modify `agents/`, rebuild wheel.

**Q: How do I update to next version?**  
A: `pip install --upgrade enterprise-agent-platform`

**Q: Does it require Docker to run?**  
A: No. Use `pip install` for local Python, or Docker if you prefer.

---

## ✅ Checklist for Publishing Your First Release

- [ ] Update version in `pyproject.toml`
- [ ] Verify tests pass: `pytest`
- [ ] Build: `python -m build`
- [ ] Test wheel locally: `pip install dist/*.whl && agent-platform --help`
- [ ] Publish to PyPI: `twine upload dist/*`
- [ ] Wait 5 min for PyPI to sync
- [ ] Verify: `pip install --index-url https://test.pypi.org enterprise-agent-platform`
- [ ] Build Docker: `docker build -f deployment/docker/Dockerfile -t myregistry/enterprise-agent-platform:VERSION .`
- [ ] Push Docker: `docker push myregistry/enterprise-agent-platform:VERSION`
- [ ] Git tag: `git tag v{VERSION} && git push origin v{VERSION}`
- [ ] Announce: "New version v{VERSION} released! `pip install --upgrade enterprise-agent-platform`"

---

## 🎓 What Your Developers Will Love

✅ **No setup complexity** — Just `pip install`  
✅ **One command to run** — `agent-platform --goal "..."`  
✅ **Reproducible** — Same behavior on any laptop/server  
✅ **Updatable** — Auto-updates with `pip install --upgrade`  
✅ **Container-ready** — Also works with Docker with zero changes  
✅ **Extensible** — Can add custom agents if needed  
✅ **Enterprise-controlled** — All execution audited, policy-enforced  

---

**You've successfully distributed an enterprise agent platform that developers can use in 10 seconds. 🚀**
