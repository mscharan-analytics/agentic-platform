"""MCP tools invocation endpoints."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list")
async def list_tools() -> dict[str, object]:
    """List all available MCP tools."""
    try:
        from agent_platform.mcp.client import get_mcp_client

        mcp = get_mcp_client()
        tools = mcp.list_tools()
        return {
            "tools": tools,
            "count": len(tools),
        }
    except Exception as e:
        logger.error(f"Error listing tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{tool_name}/invoke")
async def invoke_tool(tool_name: str, params: dict[str, Any] | None = None) -> dict[str, object]:
    """Invoke an MCP tool with the given parameters."""
    try:
        from agent_platform.mcp.client import get_mcp_client

        mcp = get_mcp_client()
        params = params or {}

        logger.info(f"Invoking tool {tool_name} with params: {params}")

        # Call tool (async)
        result = await mcp.call_tool(tool_name, **params)

        return {
            "tool": tool_name,
            "status": "success",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error invoking tool {tool_name}: {e}")
        return {
            "tool": tool_name,
            "status": "error",
            "error": str(e),
        }


@router.get("/{tool_name}/info")
async def get_tool_info(tool_name: str) -> dict[str, object]:
    """Get information about a specific MCP tool."""
    from agent_platform.mcp.client import get_mcp_client

    mcp = get_mcp_client()
    if tool_name not in mcp.list_tools():
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")

    return {
        "tool": tool_name,
        "description": f"Tool: {tool_name}",
    }
