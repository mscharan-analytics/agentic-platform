"""MCP tools for validation and deployment."""

from __future__ import annotations

from agent_platform.deployment_adapters import AzureDevOpsAdapter, GitHubActionsAdapter, JenkinsAdapter
from agent_platform.validation import StaticAnalysisAdapter


class ValidationTools:
    """MCP-registered tools for go/no-go validation."""

    @staticmethod
    async def run_static_analysis(tools: list[str]) -> dict[str, object]:
        """Execute static analysis tools (ruff, mypy, eslint)."""
        adapter = StaticAnalysisAdapter()
        results = await adapter.run(tools)
        return {
            "tools": tools,
            "results": [
                {
                    "tool": r.tool,
                    "status": r.status,
                    "findings": r.findings,
                }
                for r in results
            ],
        }


class DeploymentTools:
    """MCP-registered tools for CI/CD deployment."""

    @staticmethod
    async def trigger_github_actions(workflow: str, ref: str) -> dict[str, object]:
        """Trigger GitHub Actions workflow dispatch."""
        adapter = GitHubActionsAdapter()
        return await adapter.trigger(workflow, ref)

    @staticmethod
    async def trigger_azure_devops(pipeline: str, branch: str) -> dict[str, object]:
        """Trigger Azure DevOps pipeline run."""
        adapter = AzureDevOpsAdapter()
        return await adapter.trigger(pipeline, branch)

    @staticmethod
    async def trigger_jenkins(job_name: str, branch: str) -> dict[str, object]:
        """Trigger Jenkins build."""
        adapter = JenkinsAdapter()
        return await adapter.trigger(job_name, branch)
