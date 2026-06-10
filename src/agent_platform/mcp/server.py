from __future__ import annotations

from agent_platform.agents.catalog import default_agent_registry
from agent_platform.orchestration.hooks import HookManager
from agent_platform.orchestration.orchestrator import AutonomousRunner
from agent_platform.policy.engine import PolicyEngine
from agent_platform.mcp.integrations import IntegrationTools
from agent_platform.mcp.validation_deployment import DeploymentTools, ValidationTools

try:
    from fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit(
        "fastmcp is not installed. Install with: pip install -e .[mcp]"
    ) from exc


def build_server() -> FastMCP:
    mcp = FastMCP("enterprise-agent-platform")

    @mcp.tool(name="run_goal")
    async def run_goal(goal: str, max_steps: int = 8) -> dict[str, object]:
        registry = default_agent_registry()
        hooks = HookManager()
        policy = PolicyEngine()
        runner = AutonomousRunner(registry=registry, hooks=hooks, policy=policy)
        return await runner.run(goal=goal, max_steps=max_steps)

    @mcp.tool(name="fetch_jira_stories")
    async def fetch_jira_stories(project_key: str, max_items: int = 20) -> dict[str, object]:
        return await IntegrationTools.fetch_jira_stories(project_key, max_items)

    @mcp.tool(name="fetch_figma_spec")
    async def fetch_figma_spec(file_key: str) -> dict[str, object]:
        return await IntegrationTools.fetch_figma_spec(file_key)

    @mcp.tool(name="fetch_lucid_diagram")
    async def fetch_lucid_diagram(doc_id: str) -> dict[str, object]:
        return await IntegrationTools.fetch_lucid_diagram(doc_id)

    @mcp.tool(name="run_static_analysis")
    async def run_static_analysis(tools: list[str]) -> dict[str, object]:
        return await ValidationTools.run_static_analysis(tools)

    @mcp.tool(name="trigger_github_actions")
    async def trigger_github_actions(workflow: str, ref: str) -> dict[str, object]:
        return await DeploymentTools.trigger_github_actions(workflow, ref)

    @mcp.tool(name="trigger_azure_devops")
    async def trigger_azure_devops(pipeline: str, branch: str) -> dict[str, object]:
        return await DeploymentTools.trigger_azure_devops(pipeline, branch)

    @mcp.tool(name="trigger_jenkins")
    async def trigger_jenkins(job_name: str, branch: str) -> dict[str, object]:
        return await DeploymentTools.trigger_jenkins(job_name, branch)

    return mcp


def main() -> None:
    server = build_server()
    server.run()


if __name__ == "__main__":
    main()
