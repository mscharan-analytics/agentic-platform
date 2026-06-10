"""MCP client for agents to invoke tools."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class MCPClient:
    """Client interface for agents to call MCP tools."""

    def __init__(self) -> None:
        self._tool_registry: dict[str, Any] = {}
        self._initialize_tools()

    def _initialize_tools(self) -> None:
        """Register default tools on initialization."""
        try:
            from agent_platform.mcp.integrations import IntegrationTools

            # Register Ollama tools
            self.register_tool("ollama_list_models", IntegrationTools.ollama_list_models)
            self.register_tool("ollama_check_model", IntegrationTools.ollama_check_model)
            self.register_tool("ollama_health", IntegrationTools.ollama_health)
            self.register_tool("ollama_info", IntegrationTools.ollama_info)

            # Register integration tools
            self.register_tool("fetch_jira_stories", IntegrationTools.fetch_jira_stories)
            self.register_tool("fetch_figma_spec", IntegrationTools.fetch_figma_spec)
            self.register_tool("fetch_lucid_diagram", IntegrationTools.fetch_lucid_diagram)

            logger.debug("MCP tools initialized successfully")
        except ImportError as e:
            logger.debug(f"Some MCP tools not available: {e}")

    def register_tool(self, name: str, fn: Any) -> None:
        """Register a tool callable."""
        self._tool_registry[name] = fn
        logger.debug(f"Tool registered: {name}")

    async def call_tool(self, tool_name: str, **kwargs: Any) -> dict[str, object]:
        """Call a registered tool by name."""
        if tool_name not in self._tool_registry:
            return {"error": f"Tool {tool_name} not found", "tool": tool_name}
        fn = self._tool_registry[tool_name]
        try:
            # Handle both sync and async callables
            import inspect

            if inspect.iscoroutinefunction(fn):
                return await fn(**kwargs)
            else:
                return fn(**kwargs)
        except Exception as e:
            logger.error(f"Tool {tool_name} failed: {e}")
            return {"error": str(e), "tool": tool_name}

    def list_tools(self) -> list[str]:
        """List all registered tools."""
        return list(self._tool_registry.keys())


# Singleton instance for agents to use
_mcp_client = MCPClient()


def get_mcp_client() -> MCPClient:
    """Get the global MCP client instance."""
    return _mcp_client

