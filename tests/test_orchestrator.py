import asyncio

from agent_platform.agents.catalog import default_agent_registry
from agent_platform.mcp import initialize_mcp_client
from agent_platform.orchestration.hooks import HookManager
from agent_platform.orchestration.orchestrator import AutonomousRunner
from agent_platform.policy.engine import PolicyEngine


def test_autonomous_runner_completes() -> None:
    initialize_mcp_client()
    registry = default_agent_registry()
    hooks = HookManager()
    policy = PolicyEngine()
    runner = AutonomousRunner(registry=registry, hooks=hooks, policy=policy)

    result = asyncio.run(runner.run(goal="Implement secure flow", max_steps=4))

    assert "trace_id" in result
    assert len(result["steps"]) >= 1
    assert result["audit_events"] >= 4


def test_sdlc_pipeline_completes_when_validation_passes() -> None:
    initialize_mcp_client()
    registry = default_agent_registry()
    hooks = HookManager()
    policy = PolicyEngine()
    runner = AutonomousRunner(registry=registry, hooks=hooks, policy=policy)

    result = asyncio.run(
        runner.run_sdlc_pipeline(
            goal="Build approval automation",
            target_env="staging",
            max_validation_retries=2,
            fail_until_attempt=0,
        )
    )

    assert result["status"] == "completed"
    stage_names = [item["stage"] for item in result["stages"]]
    assert "requirements_intake" in stage_names
    assert "validation" in stage_names
    assert "deploy" in stage_names


def test_sdlc_pipeline_blocks_when_validation_never_passes() -> None:
    initialize_mcp_client()
    registry = default_agent_registry()
    hooks = HookManager()
    policy = PolicyEngine()
    runner = AutonomousRunner(registry=registry, hooks=hooks, policy=policy)

    result = asyncio.run(
        runner.run_sdlc_pipeline(
            goal="Build release train",
            target_env="prod",
            max_validation_retries=1,
            fail_until_attempt=10,
        )
    )

    assert result["status"] == "blocked_no_go"
    stage_names = [item["stage"] for item in result["stages"]]
    assert "deploy" not in stage_names
