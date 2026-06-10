# Documentation

## Purpose
Curate, organize, and maintain all project documentation. Ensure accuracy, completeness, and accessibility for users, contributors, and stakeholders.

## Current State
**Status:** Architecture docs complete; missing operational guides

### Documentation Inventory

| Document | Status | Purpose |
|----------|--------|---------|
| 01-ARCHITECTURE.md | ✅ Complete | High-level platform design |
| 02-QUICK-START.md | ✅ Complete | New user onboarding |
| 03-STRUCTURE.md | ✅ Complete | Repository layout explanation |
| 04-DISTRIBUTION.md | ✅ Complete | Deployment models overview |
| 05-DISTRIBUTION-MODELS.md | ✅ Complete | Detailed distribution strategies |
| 06-DEVELOPER-ONBOARDING.md | ✅ Complete | Contributor setup guide |
| 07-COMPLETE-SUMMARY.md | ✅ Complete | Project summary |
| 08-VISION-ALIGNMENT.md | ✅ Complete | Strategic alignment document |
| 09-MCP-INTEGRATION.md | ✅ Complete | MCP architecture guide |
| 10-REPO-RUNTIME-FLOW.mmd | ✅ Complete | Sequence diagram (execution flow) |
| 11-CICD.md | ✅ Complete | CI/CD pipeline documentation |
| 12-HIGH-LEVEL-ARCHITECTURE.mmd | ✅ Complete | Architecture diagram |
| 13-HOW-TO-USE.md | ✅ Complete | User feature guide |
| README.md | ✅ Complete | GitHub repository intro |
| DISTRIBUTION-REFERENCE.md | ✅ Complete | Deployment reference |

### Missing Documentation
- Persistent Project Brain system (currently being created)
- Production deployment runbook (needed)
- MCP tool development guide (needed)
- Troubleshooting guide (needed)
- API reference for custom agents (needed)
- Security operations guide (needed)

### Documentation Style
- **Format:** Markdown with embedded diagrams (Mermaid)
- **Tone:** Technical, precise, example-driven
- **Organization:** Sequential numbering for reading order (01-, 02-, etc.)

## Active Decisions

### Decision: Mermaid for Diagrams
- **Adopted:** Use Mermaid.js for all diagrams
- **Rationale:** First-class text format, version control friendly, GitHub rendering
- **Status:** Applied to architecture and runtime flow docs

### Decision: Sequential Organization
- **Adopted:** Prefix docs with numbers (01-, 02-, etc.) for recommended reading order
- **Rationale:** Guides new readers through context progressively
- **Status:** Applied; see document inventory above

### Decision: Vault-Hosted Execution Plans
- **Adopted:** Execution plans live in vault/, not docs/
- **Rationale:** Execution docs are operational, not reference docs
- **Status:** Implementing now with Persistent Project Brain system

## Owned Assets

### Code
- `docs/` directory - All markdown documentation
- Diagram sources (embedded in markdown as Mermaid blocks)

### Metadata
- This index file
- Execution plan (in vault)
- Handoff notes (in vault)

## Documentation Roadmap

### Planned Additions
1. **Production Deployment Runbook** - Step-by-step for first deployment
2. **Troubleshooting Guide** - Common issues and solutions
3. **MCP Tool Development** - How to write custom MCP integrations
4. **Security Operations** - Running the platform securely in production
5. **API Reference** - CustomAgent development guide

### Maintenance Schedule
- **Review Cycle:** Quarterly (every 3 months)
- **Update Trigger:** After major feature additions or architectural changes
- **Validation:** Link checking, code example verification

## Risks & Blockers
- **MEDIUM:** Operational docs (runbooks, troubleshooting) not written → high friction for early operators
- **LOW:** No API reference for custom agents → harder for extension development

## Change Log
- **2026-04-10:** Documentation index created during brain system initialization
