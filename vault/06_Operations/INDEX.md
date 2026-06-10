# Operations

## Purpose
Manage deployment infrastructure, runtime systems, CI/CD pipelines, monitoring, and operational excellence of the platform.

## Current State
**Status:** Self-hosted execution model, Docker-based deployment ready

### Deployment Model
- **Target:** Self-hosted runners (enterprise on-prem or private clouds)
- **Container:** Docker image available (see `deployment/docker/`)
- **Orchestration:** Docker Compose file for local dev/demo
- **Production Deployment:** Needs formal runbook

### CI/CD Pipeline
- **VCS:** GitHub (public repository)
- **Runner Type:** Self-hosted (GitHub-hosted capacity unavailable)
- **Build Artifacts:** Docker image, Python package (on PyPI)
- **Release Process:** Manual (via GitHub releases)

### Observability
- **Logging:** Currently stdout/stderr to console
- **Metrics:** Not collected
- **Tracing:** Hook system enables tracing, but not persisted
- **Dashboards:** None yet

### Infrastructure
- **Database:** None (stateless design)
- **Storage:** File-based vault and state
- **Backup:** Manual (via git)
- **Disaster Recovery:** None formalized

## Active Decisions

### Decision: Self-Hosted Runners Only
- **Adopted:** Skip GitHub-hosted runner capacity
- **Rationale:** Aligns with on-prem product positioning; cost efficiency
- **Status:** CI/CD workflows retargeted (recent PR merge)
- **Impact:** Contributors need self-hosted runner access

### Decision: Stateless Execution
- **Adopted:** No persistent state across sessions (yet)
- **Rationale:** Simplifies deployment; enables horizontal scaling
- **Status:** Architecture complete; Persistent Brain system under construction to repair this

### Decision: Docker-First
- **Adopted:** All deployments containerized
- **Rationale:** Ensures reproducibility, simplifies on-prem installation
- **Status:** Dockerfile complete, Docker Compose provided

## Owned Assets

### Code
- `deployment/docker/Dockerfile` - Container image definition
- `deployment/docker/docker-compose.yml` - Local dev setup
- `.github/workflows/` - CI/CD pipeline definitions
- `scripts/quality.sh`, `scripts/test.sh` - Validation scripts

### Documentation
- `docs/11-CICD.md` - CI/CD architecture and runbooks
- `docs/02-QUICK-START.md` - Setup instructions

### Infrastructure
- PyPI publish workflow (needs formalization)
- Docker Hub push workflow (if applicable)

## Needs

1. **Production deployment runbook** - Step-by-step guide for first deployment
2. **Monitoring system** - Collect and visualize platform health
3. **Backup/recovery procedures** - Protect vault and state
4. **Scaling guidelines** - How to add runner capacity, manage load
5. **Incident response plan** - What to do when deployment fails

## Risks & Blockers
- **HIGH:** No formal production deployment guide → risky for first customer
- **MEDIUM:** No monitoring/alerting → can't detect platform issues
- **MEDIUM:** Manual release process → error-prone, low velocity
- **LOW:** Self-hosted runner dependency → coordination overhead for contributors

## Change Log
- **2026-04-10:** Operations index created during brain system initialization
- Recent: Self-hosted runner CI/CD retargeting merged
