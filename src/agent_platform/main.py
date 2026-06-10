from __future__ import annotations

import argparse
import asyncio
import json
import logging

from agent_platform.agents.catalog import default_agent_registry
from agent_platform.mcp import initialize_mcp_client
from agent_platform.orchestration.hooks import HookManager
from agent_platform.orchestration.orchestrator import AutonomousRunner
from agent_platform.policy.engine import PolicyEngine

logger = logging.getLogger(__name__)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Enterprise Agent Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Execute goal command
    run_parser = subparsers.add_parser("run", help="Execute an autonomous goal")
    run_parser.add_argument("--goal", required=True, help="Objective the autonomous runner should execute")
    run_parser.add_argument("--max-steps", type=int, default=8, help="Maximum worker loop iterations")

    # API server command
    api_parser = subparsers.add_parser("api", help="Start REST API server")
    api_parser.add_argument("--port", type=int, default=8000, help="API server port")
    api_parser.add_argument("--host", default="0.0.0.0", help="API server host")

    # Legacy: support --goal without subcommand for backwards compatibility
    parser.add_argument("--goal", help="Objective (legacy, use 'run' command)")
    parser.add_argument("--max-steps", type=int, default=8, help="Maximum worker loop iterations")

    return parser


async def _run_goal(goal: str, max_steps: int) -> dict[str, object]:
    """Execute a goal using the autonomous runner."""
    initialize_mcp_client()
    registry = default_agent_registry()
    hooks = HookManager()
    policy = PolicyEngine()
    runner = AutonomousRunner(registry=registry, hooks=hooks, policy=policy)
    return await runner.run(goal=goal, max_steps=max_steps)


def _run_api(host: str, port: int) -> None:
    """Start the FastAPI server."""
    import uvicorn

    from agent_platform.api.server import create_app

    app = create_app()
    uvicorn.run(app, host=host, port=port)


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    # Legacy mode: if --goal provided without subcommand
    if args.goal and args.command is None:
        logger.warning("Using legacy mode. Consider using: agent-platform run --goal '...'")
        result = asyncio.run(_run_goal(goal=args.goal, max_steps=args.max_steps))
        print(json.dumps(result, indent=2))
        return

    # New subcommand mode
    if args.command == "run":
        result = asyncio.run(_run_goal(goal=args.goal, max_steps=args.max_steps))
        print(json.dumps(result, indent=2))
    elif args.command == "api":
        _run_api(host=args.host, port=args.port)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
