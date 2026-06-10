# Community

## Purpose
Foster developer experience, onboarding, contribution pathways, and community-driven evolution of the platform.

## Current State
**Status:** Foundation in place, community adoption beginning

### Developer Onboarding
- **Onboarding Guide:** `docs/06-DEVELOPER-ONBOARDING.md` available
- **Setup Complexity:** Moderate - requires Python, Docker, and basic agent architecture knowledge
- **Time to First Demo:** ~15 minutes with `scripts/demo.sh`
- **Known Friction Points:** MCP setup complexity, policy engine obscurity

### Contribution Model
- **Repository:** Public (GitHub)
- **License:** As specified in repo LICENSE file
- **Contributor Guidelines:** Not formally documented
- **Code Review:** Informal currently

### Community Assets
- Issue tracking (bugs, features)
- Pull request workflow
- Discussion board (GitHub Discussions - not yet used)

## Active Decisions

### Decision: Low-Barrier Entry
- **Adopted:** Simple demo script, clear setup instructions, extensive README
- **Rationale:** Lower friction = higher adoption
- **Status:** Working, but can be improved

### Decision: Self-Hosted Runners
- **Adopted:** CI/CD uses self-hosted runners, not GitHub-hosted
- **Rationale:** Aligns with product positioning; avoids cloud vendor lock-in
- **Impact:** Higher setup complexity for contributors
- **Status:** Implemented (PR #XXXX merged)

## Owned Assets

### Documentation
- `docs/06-DEVELOPER-ONBOARDING.md` - Setup and contribution guide
- `/scripts/` - Demo, test, quality, bootstrap scripts
- README.md - High-level project intro

### Issue & PR Triage
- Currently unfilitered; needs triage process

### Community Channels
- GitHub Discussions (planned activation)
- Contributing guidelines (needs creation)

## Needs

1. **Contribution workflow** - Define process for PRs, issues, releases
2. **Triage process** - Who reviews, prioritizes, assigns work?
3. **Community onboarding** - For external contributors
4. **Feedback channels** - How do users report issues / request features?

## Risks & Blockers
- No structured feedback mechanism → hard to understand user needs
- Contributor guidelines missing → might reject well-intentioned PRs
- Demo setup still has friction → could deter new users

## Change Log
- **2026-04-10:** Community index created during brain system initialization
