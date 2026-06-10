# Enterprise Agent Platform - Distribution Reference Card

## The Core Answer

**Problem:** "How do developers use this without cloning and managing source files?"

**Solution:** 
- Developers never see source code
- They install a 27 KB Python wheel via `pip install`
- Or they run a Docker image with zero setup
- One command, autonomous execution

---

## Three Paths Forward

### Path 1: Publish to PyPI (Simplest for Public)
```bash
# One-time setup:
# - Create PyPI account (pypi.org)
# - Store token in ~/.pypi credentials

# Per release:
python -m build
twine upload dist/*

# Developer then:
pip install enterprise-agent-platform
```

### Path 2: Private PyPI (Enterprise Internal)
```bash
# One-time setup:
# - Set up internal PyPI (e.g., Artifactory, Nexus)
# - Get repo URL + credentials

# Per release:
python -m build
twine upload --repository-url https://internal.pypi.company.com dist/*

# Developer then:
pip install -i https://internal.pypi.company.com enterprise-agent-platform
```

### Path 3: Docker Registry (Container)
```bash
# One-time setup:
# - Docker account or private registry access
# - Registry credentials configured

# Per release:
docker build -f deployment/docker/Dockerfile \
  -t myregistry.com/enterprise-agent-platform:0.1.0 .
docker push myregistry.com/enterprise-agent-platform:0.1.0

# Developer then:
docker run myregistry.com/enterprise-agent-platform --goal "..."
```

---

## Distribution Checklist (Per Release)

- [ ] Increment version in `pyproject.toml`
- [ ] Run tests: `pytest`
- [ ] Build: `python -m build`
- [ ] Test locally: `pip install dist/*.whl && agent-platform --help`
- [ ] Publish wheel: `twine upload dist/*` (to your target)
- [ ] Build Docker: `docker build -f deployment/docker/Dockerfile -t ... .`
- [ ] Push Docker: `docker push ...`
- [ ] Tag git: `git tag v0.X.Y && git push origin v0.X.Y`
- [ ] Notify developers via email/Slack with onboarding doc

---

## What Gets Distributed

| Artifact | Size | Format | Installation |
|----------|------|--------|--------------|
| Wheel | 27 KB | `.whl` | `pip install` |
| Source | 25 KB | `.tar.gz` | `pip install` from URL |
| Docker | 150 MB | Image | `docker pull` + `docker run` |

---

## Developer Experience After Release

### Scenario 1: "Just Use It" Developer
```bash
$ pip install enterprise-agent-platform
Collecting enterprise-agent-platform
  Downloading enterprise_agent_platform-0.1.0-py3-none-any.whl (27 kB)
Installing collected packages: enterprise-agent-platform, pydantic
Successfully installed enterprise-agent-platform-0.1.0

$ agent-platform --goal "Deploy with policy checks"
trace_id: a1b2c3d4-e5f6-4789-abc0-def123456789
solver: ✓ Decomposed objective into constraints
planner: ✓ Created 8-step execution DAG
steps completed: 3
evaluation: ✓ All quality gates passed
audit_events: 12
```

### Scenario 2: "Docker-First" DevOps Engineer
```bash
$ docker pull myregistry.com/enterprise-agent-platform:latest

$ docker run -e OLLAMA_BASE_URL=http://ollama:11434 \
  myregistry.com/enterprise-agent-platform \
  --goal "Deploy service X"

[outputs same autonomous execution]
```

### Scenario 3: "Learner/Contributor" Developer
```bash
$ git clone https://github.com/yourorg/enterprise-agent-platform
$ cd enterprise-agent-platform
$ pip install -e .[dev]
$ pytest                  # Run tests
$ agent-platform --goal "Test goal"  # Try locally
$ # [Edit agents, run tests, contribute back]
```

---

## Distribution Timeline

```
Week 1: Setup & Testing
  ├── Verify all tests pass
  ├── Verify wheel builds & installs locally
  └── Test Docker build

Week 2: Infrastructure
  ├── Configure PyPI/internal package repo credentials
  ├── Configure Docker registry secrets
  └── Test CI/CD automation (GitHub Actions)

Week 3: Release
  ├── Tag v0.1.0 in GitHub
  ├── GitHub Actions auto-builds & publishes (if CI/CD configured)
  ├── OR manually: python -m build && twine upload dist/*
  ├── OR manually: docker build && docker push
  └── Publish onboarding doc to team

Week 4+: Developer Adoption
  ├── Developers: pip install enterprise-agent-platform
  ├── Developers: docker run enterprise-agent-platform
  ├── Gather feedback
  └── Plan v0.2.0 improvements
```

---

## File Locations (Quick Reference)

| What | Where |
|------|-------|
| **Main entry point** | `src/agent_platform/main.py` |
| **All 12 agents** | `src/agent_platform/agents/{agent_type}/` |
| **Protocols (ACP/A2A)** | `src/agent_platform/contracts/` |
| **Policy engine** | `src/agent_platform/policy/engine.py` |
| **Model routing** | `src/agent_platform/model_gateway/` |
| **Package config** | `pyproject.toml` |
| **Docker build** | `deployment/docker/Dockerfile` |
| **Docker compose** | `deployment/docker/docker-compose.yml` |
| **Test suite** | `tests/` |
| **CLI scripts** | `scripts/` |
| **Documentation** | `docs/` |
| **Distribution artifacts** | `dist/` (built via `python -m build`) |

---

## Troubleshooting

**Q: Wheel fails on install locally → "ModuleNotFoundError"**  
A: Wheel build is corrupted. Rebuild: `python -m build` and reinstall.

**Q: Docker build fails → "COPY src/ no match"**  
A: Ensure Dockerfile is in repo root context. Rebuild with: `docker build -f deployment/docker/Dockerfile .`

**Q: Developer installs old version**  
A: They need latest: `pip install --upgrade enterprise-agent-platform`

**Q: Docker image huge?**  
A: Expected (~150 MB includes Python + deps). Use multi-stage build if needed.

---

## Cost of Ownership

| Activity | Frequency | Effort | Notes |
|----------|-----------|--------|-------|
| Release (build + publish) | Per version | 5 min | Mostly automated |
| Documentation update | Per version | 10 min | Update version #s |
| Support (developer Q&A) | Ongoing | 10-30 min/week | Share onboarding doc |
| Bug fixes | As needed | Variable | Normal dev cycle |
| Feature requests | As needed | Variable | Plan v0.2, v0.3, etc. |

---

## Success Metrics

Track these after release:

```
✓ Developer installation success rate (target: 99%)
✓ Time from install to first successful run (target: <5 min)
✓ Autonomous execution success rate (target: >95%)
✓ Policy enforcement accuracy (target: 100%)
✓ Audit trail completeness (target: 100%)
✓ Support tickets volume (target: <10% of users)
```

---

## Commands Cheat Sheet

```bash
# Build and test
python -m build
pip install dist/*.whl
agent-platform --help
pytest

# Publish to PyPI
twine upload dist/*

# Build Docker
docker build -f deployment/docker/Dockerfile -t myregistry/agent-platform:0.1.0 .

# Run Docker
docker run -it myregistry/agent-platform --goal "Your goal"

# Local development
pip install -e .[dev]
pytest -v
bash scripts/quality.sh
```

---

**Version:** 0.1.0  
**Last Updated:** April 7, 2026  
**Status:** Ready for Production Release 🚀
