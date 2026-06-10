# Persistent Project Context

## Business Context
- EMSP is a multi-repo platform for campaign authoring, proofing, approvals, reporting, and admin workflows.
- Shell-hosted MFE architecture with strict repo ownership and RBAC boundaries.
- Cross-repo sequencing is mandatory: core -> services -> remotes -> shell.

## Operating Defaults
- Use problem routing first when request is ambiguous.
- Use system routing rules before cross-repo changes.
- Enforce session/context/token governance for autonomous runs.

## Update Rule
This file should only contain stable context that remains useful across sessions.
Session-specific details must go into `.github/context/summaries/SESSION-LATEST.md`.
