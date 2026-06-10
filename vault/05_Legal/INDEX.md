# Legal & Compliance

## Purpose
Manage licensing, compliance, data handling, intellectual property, and regulatory requirements for the platform and its use by enterprises.

## Current State
**Status:** Baseline - needs audit and formalization

### Licensing
- **Repository License:** Defined in LICENSE file
- **Dependency Licenses:** Tracked in requirements files (needs audit)
- **Status:** No license conflict review completed

### Compliance Posture
- **Data Handling:** Platform processes user code, logs, and LLM prompts
- **Data Retention:** No policy defined
- **Data Deletion:** No process defined
- **Audit Trail:** Hook/policy system enables audit, not yet formalized

### Intellectual Property
- **Source Code:** Licensed under repo license (see LICENSE)
- **Trademarks:** "Enterprise Agent Platform" - not registered
- **Patents:** No patent strategy

### Security & Privacy
- **Privacy Policy:** Not published
- **Terms of Service:** Not published
- **Security Model:** Documented in `vault/07_Security/`

## Active Decisions

### Decision: Licensing Strategy
- **Current State:** Open-source license applied
- **Rationale:** Enable community innovation and transparency
- **Outstanding Decision:** Enterprise licensing model (commercial variant?)

### Decision: Data Handling in LLM Integration
- **Outstanding:** How is user code sent to LLM providers? What guarantees needed?
- **Impact:** Critical for enterprise adoption
- **Priority:** High

## Owned Assets

### Governance Documents
- LICENSE file in repo
- (Privacy Policy - needs creation)
- (Terms of Service - needs creation)
- (Data Processing Agreement template - needs creation)

### Compliance Checklist
- [ ] Audit all dependencies for license conflicts
- [ ] Review LLM data handling practices
- [ ] Publish privacy policy
- [ ] Publish terms of service
- [ ] Create data processing agreement for enterprise customers

## Risks & Blockers
- **HIGH:** No LLM data handling policy → enterprise adoption at risk
- **HIGH:** License conflicts not audited → potential IP violations
- **MEDIUM:** Privacy/ToS not published → legal uncertainty
- **MEDIUM:** No data retention policy → compliance gaps

## Change Log
- **2026-04-10:** Legal index created during brain system initialization
