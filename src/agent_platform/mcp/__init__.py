"""Initialize MCP client with all registered tools."""

from __future__ import annotations

from agent_platform.mcp.client import get_mcp_client
from agent_platform.mcp.integrations import IntegrationTools
from agent_platform.mcp.validation_deployment import DeploymentTools, ValidationTools


def initialize_mcp_client() -> None:
    """Register all tools with the MCP client."""
    client = get_mcp_client()

    # Integration tools
    client.register_tool("fetch_jira_stories", IntegrationTools.fetch_jira_stories)
    client.register_tool("fetch_figma_spec", IntegrationTools.fetch_figma_spec)
    client.register_tool("fetch_lucid_diagram", IntegrationTools.fetch_lucid_diagram)

    # Validation tools
    client.register_tool("run_static_analysis", ValidationTools.run_static_analysis)

    # Deployment tools
    client.register_tool("trigger_github_actions", DeploymentTools.trigger_github_actions)
    client.register_tool("trigger_azure_devops", DeploymentTools.trigger_azure_devops)
    client.register_tool("trigger_jenkins", DeploymentTools.trigger_jenkins)
