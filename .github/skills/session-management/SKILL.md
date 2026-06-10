# Session Management Skill

## Goal
Provide deterministic session lifecycle control for long autonomous runs.

## When To Use
- Multi-stage workflows
- Resume/retry requirements
- Interrupted or flaky execution environments

## Required Outputs
- Session metadata model
- Checkpoint model
- Resume policy
- Failure recovery policy

## Session Schema
- session_id
- run_id
- started_at
- current_stage
- completed_stages
- pending_stages
- checkpoint_ref
- recovery_notes
