# How Developers Actually Use This (Distribution Models)

## TL;DR: 3 Ways Developers Get Started

| Method | Setup Time | Dependencies | Use Case |
|--------|-----------|--------------|----------|
| **pip install** | 10 seconds | Python 3.11+ | Individual developers, laptops |
| **Docker** | 30 seconds | Docker only | Laptops, servers, CI/CD |
| **Source (dev)** | 2 minutes | Python 3.11+ + git | Contributors, customization |

---

## Option 1: pip install (Production/Most Common)

### For End Users
```bash
pip install enterprise-agent-platform
agent-platform --goal "Deploy feature X safely"
```

**What happens behind the scenes:**
1. Python package manager downloads 27 KB wheel from PyPI
2. Extracts to site-packages
3. Creates `agent-platform` CLI entry point
4. Done! Can run immediately

**Benefits:**
- ✅ One-liner
- ✅ No clone, no files to manage
- ✅ Works on any OS
- ✅ Auto-updates with `pip install --upgrade`

**How to distribute:**
```bash
# Package maintainer does this once per release
python -m build
twine upload dist/*  # Goes to PyPI

# OR upload to private PyPI:
twine upload --repository-url https://internal-pypi.company.com dist/*
```

**Developer experience:**
```bash
# Developer:
$ pip install enterprise-agent-platform
$ agent-platform --goal "Implement feature..."
trace_id: xyz...
[autonomous execution completes]
```

---

## Option 2: Docker Image (No Python Required)

### For End Users
```bash
docker pull enterprise-agent-platform:latest
docker run -it enterprise-agent-platform --goal "Your objective"
```

**What happens:**
1. Docker image contains Python + all deps + package
2. Runs in isolation
3. No local Python needed

**Benefits:**
- ✅ Zero local setup
- ✅ Works on Linux/Mac/Windows
- ✅ Reproducible & locked versions
- ✅ Easy to orchestrate in Kubernetes/Cloud

**How to distribute:**
```bash
# Package maintainer:
docker build -f deployment/docker/Dockerfile -t enterprise-agent-platform:0.1.0 .
docker tag enterprise-agent-platform:0.1.0 enterprise-agent-platform:latest
docker push docker.io/yourorg/enterprise-agent-platform:latest

# OR private registry:
docker push internal-registry.company.com/enterprise-agent-platform:latest
```

**Developer experience:**
```bash
# Developer:
$ docker run enterprise-agent-platform --goal "Deploy with checks"
[no Python, no config needed]
```

---

## Option 3: Source Install (Development/Customization)

### For Contributors
```bash
git clone https://github.com/yourorg/enterprise-agent-platform.git
cd enterprise-agent-platform
pip install -e .
agent-platform --goal "Your goal"
```

**What happens:**
1. Clones source repo
2. `pip install -e .` creates editable install (points to source)
3. Changes to source are reflected immediately
4. Tests added are runnable

**Benefits:**
- ✅ Full source control
- ✅ Can customize agents
- ✅ Can run tests
- ✅ Can contribute back

---

## How Each Model Works Technically

### Model 1: pip install from PyPI

```
Developer Laptop
  ↓
  pip install enterprise-agent-platform
  ↓
PyPI (pypi.org)
  ↓
  Downloads: enterprise_agent_platform-0.1.0-py3-none-any.whl
  ↓
  ~/.local/lib/python3.11/site-packages/agent_platform/
  ↓
  agent-platform CLI available
  ↓
  Ready to run ✅
```

**Packaging steps (happened once by maintainer):**
```bash
$ python -m build          # Creates .whl + .tar.gz
$ twine upload dist/*      # Upload to PyPI
```

### Model 2: Docker Image

```
Developer Laptop
  ↓
  docker pull enterprise-agent-platform:latest
  ↓
  Docker Registry (docker.io or private)
  ↓
  Downloads image (Dockerfile + Python + package + entrypoint)
  ↓
  docker run ...
  ↓
  Python env spun up in container
  ↓
  agent-platform executes
  ↓
  Results returned ✅
```

**Packaging steps (happened once by maintainer):**
```bash
$ docker build -f deployment/docker/Dockerfile \
    -t enterprise-agent-platform:0.1.0 .  # Creates image
$ docker push docker.io/yourorg/enterprise-agent-platform:0.1.0  # Publish
```

### Model 3: Source

```
Developer Laptop
  ↓
  git clone <repo>
  ↓
  pip install -e .         # Editable install -> ./src/
  ↓
  ~/.local/bin/agent-platform -> ../site-packages/../src/...
  ↓
  agent-platform command runs from source
  ↓
  Changes reflected immediately (dev editing)
  ↓
  Ready to test + commit ✅
```

---

## Production Workflow (For Ops)

### Step 1: Developer Pushes Tag
```bash
git tag v0.2.0
git push origin v0.2.0
```

### Step 2: GitHub Actions Auto-Builds
(See `.github/workflows/release.yml`)
- Builds Python wheel
- Builds Docker image
- Uploads wheel to PyPI
- Pushes image to registry

### Step 3: Developers Can Install (Any Model)
```bash
# Model 1: pip
pip install --upgrade enterprise-agent-platform

# Model 2: Docker
docker pull enterprise-agent-platform:latest

# Model 3: Source
git checkout v0.2.0
pip install -e .
```

---

## Quick Reference: What Gets Deployed

### pip Package (27 KB .whl)
```
enterprise_agent_platform-0.1.0-py3-none-any.whl
├── agent_platform/
│   ├── agents/          # All 12 agent modules
│   ├── contracts/       # ACP, A2A protocols
│   ├── orchestration/   # Runner, hooks
│   ├── policy/          # RBAC enforcement
│   ├── model_gateway/   # Ollama routing
│   ├── security/        # Audit trails
│   ├── telemetry/       # Metrics
│   └── main.py          # CLI entry
├── agent_platform.dist-info/  # Metadata
```

### Docker Image (~150 MB)
```
FROM python:3.11-slim
├── Python 3.11 + apt packages
├── pip dependencies (pydantic, etc.)
├── Extracted wheel contents
├── COPY src/ + tests/
├── ENTRYPOINT agent-platform
```

---

## Frequently Asked

**Q: What if I don't want to use PyPI?**  
A: Use Docker image or `pip install ./dist/enterprise_agent_platform-0.1.0-py3-none-any.whl`

**Q: What if I need to customize agents?**  
A: Clone source, modify `src/agent_platform/agents/`, rebuild wheel.

**Q: Can I use this offline?**  
A: Yes with both pip and Docker (Ollama runs locally).

**Q: Do I download source code whenever I run it?**  
A: No. Once installed (pip or docker), code is cached locally.

**Q: What about version pinning?**  
A: `pip install enterprise-agent-platform==0.1.0` or Docker tag it.

---

## Summary for Your Enterprise

**Tell developers:**
> "🚀 Getting started is simple. Pick your style:
>
> **Laptop?** → `pip install enterprise-agent-platform`  
> **Container?** → `docker run enterprise-agent-platform`  
> **Contributing?** → Clone repo, `pip install -e .`
>
> Then just run: `agent-platform --goal 'Your objective'`"
