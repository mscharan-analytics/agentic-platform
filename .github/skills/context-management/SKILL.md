# Context Management Skill

## Goal
Build and maintain high-quality context packs with minimal noise.

## When To Use
- Large repositories
- Multi-agent handoffs
- Tasks requiring provenance and relevance controls

## Context Tiers
1. static_context: policy, architecture, governance
2. working_context: current task files and decisions
3. memory_context: prior session outcomes and lessons

## Guardrails
- Exclude secrets
- Prefer local repo references
- Add provenance to external references
- Enforce TTL for stale context
