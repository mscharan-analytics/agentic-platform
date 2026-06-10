# Security

## Purpose
Protect platform architecture, user data, supply chain integrity, and operational security. Identify and mitigate threats. Ensure enterprise security compliance.

## Current State
**Status:** Foundation in place, needs production hardening

### Security Architecture
- **Authentication:** Local execution only (no auth layer yet)
- **Authorization:** Policy engine provides access control framework
- **Encryption:** No encryption at rest/transit (runs locally)
- **Secret Management:** Env vars only (no vault integration)
- **Audit Trail:** Hook system enables audit; not formalized

### Known Security Posture
- **Threat Model:** Self-hosted, trusted operator environment assumed
- **Attack Surface:** MCP tool integrations (potential code injection)
- **Data at Risk:** User code, execution logs, prompts sent to LLMs

### Dependency Security
- **Vulnerability Scanning:** Not automated
- **Dependency Updates:** Manual process
- **SBOM:** Not generated
- **Supply Chain Policy:** Not formalized

## Active Decisions

### Decision: Local-Only Execution
- **Adopted:** No authentication required; assume trusted operator
- **Rationale:** Simplifies security model for on-prem deployment
- **Status:** Enforced by architecture
- **Impact:** Enterprise users must secure their own infrastructure

### Decision: MCP Tool Sandboxing
- **Outstanding Decision:** How to prevent malicious MCP tools from compromising platform?
- **Current State:** No validation; tool registration is open
- **Priority:** HIGH - needed before production

### Decision: LLM Data Handling
- **Outstanding Decision:** Can user code be sent to external LLM providers? What safeguards?
- **Current State:** Undecided; ModelGateway not yet wired
- **Priority:** CRITICAL - blocks enterprise adoption

## Owned Assets

### Code
- `src/agent_platform/security/` - Security module (stub)
- `src/agent_platform/policy/engine.py` - Policy enforcement
- `src/agent_platform/orchestration/hooks.py` - Audit trail capability

### Documentation
- `docs/01-ARCHITECTURE.md` - High-level architecture (includes security sections)
- (Threat model - needs creation)
- (Security runbook - needs creation)

### Processes
- Dependency update schedule (informal)
- Security incident contact (not published)

## Security Needs

1. **Threat Model** - Formalize threats, mitigations, and assumptions
2. **MCP Tool Validation** - Whitelist/sandbox MCP integrations
3. **LLM Data Policy** - Define what data can be sent to external LLMs
4. **SBOM Generation** - Track dependencies for supply chain visibility
5. **Automated Scanning** - Integrate dependency and SAST scanning to CI/CD
6. **Audit Logging** - Persist hook-based audit trail to secure store
7. **Secrets Management** - Integrate HashiCorp Vault or similar
8. **Production Hardening** - Security review before first production deployment

## Risks & Blockers
- **CRITICAL:** No LLM data handling policy → regulatory risk
- **HIGH:** MCP tools not validated → code injection vector
- **HIGH:** No automated vulnerability scanning → supply chain risk
- **HIGH:** Audit trail not persisted → no compliance trail
- **MEDIUM:** Secret management is ad-hoc → credential exposure risk
- **MEDIUM:** No threat model → can't prioritize mitigations

## Compliance Requirements

### Enterprise Deployments Must Satisfy
- [ ] Data residency (code stays on customer infrastructure)
- [ ] Audit trail (immutable record of all actions)
- [ ] Encryption (data at rest on disk)
- [ ] Access controls (who can submit jobs, view logs?)

## Change Log
- **2026-04-10:** Security index created during brain system initialization
