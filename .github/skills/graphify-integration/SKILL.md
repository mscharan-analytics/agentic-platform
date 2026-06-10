# Graphify Integration Skill

## Goal
Apply graph orchestration for robust autonomous execution with branching and recovery.

## Reference
- https://github.com/safishamsi/graphify

## When To Use
- Branching task execution
- Retry and compensation logic
- Stateful orchestration across sessions

## Node Contract
- node_id
- description
- inputs
- outputs
- success_transition
- failure_transition
- retry_policy

## Required Outputs
- Node/edge map
- Retry strategy
- Error transitions
- Trace schema for audit
