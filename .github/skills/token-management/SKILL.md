# Token Management Skill

## Goal
Control token budget and prevent runaway execution costs.

## When To Use
- Long or multi-stage workflows
- High-complexity prompts
- Nested planning and generation tasks

## Budget Policy
- Estimate by stage before execution
- Reserve headroom for verification and audit
- Trigger split-session plan when threshold exceeded

## Required Outputs
- Budget table by stage
- Hard limits and stop conditions
- Compression strategy
- Session split strategy when needed
