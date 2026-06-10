"""Ollama service management endpoints."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
async def get_ollama_health() -> dict[str, object]:
    """Get Ollama service health status."""
    try:
        from agent_platform.mcp.client import get_mcp_client

        mcp = get_mcp_client()
        result = await mcp.call_tool("ollama_health")
        return result
    except Exception as e:
        logger.error(f"Error checking Ollama health: {e}")
        return {
            "service_available": False,
            "error": str(e),
        }


@router.get("/models")
async def list_ollama_models() -> dict[str, object]:
    """List all Ollama models."""
    try:
        from agent_platform.mcp.client import get_mcp_client

        mcp = get_mcp_client()
        result = await mcp.call_tool("ollama_list_models")
        return result
    except Exception as e:
        logger.error(f"Error listing Ollama models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/{model_name}/check")
async def check_ollama_model(model_name: str) -> dict[str, object]:
    """Check if a specific Ollama model is available."""
    try:
        from agent_platform.mcp.client import get_mcp_client

        mcp = get_mcp_client()
        result = await mcp.call_tool("ollama_check_model", model_name=model_name)
        return result
    except Exception as e:
        logger.error(f"Error checking model {model_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/info")
async def get_ollama_info() -> dict[str, object]:
    """Get Ollama service information."""
    try:
        from agent_platform.mcp.client import get_mcp_client

        mcp = get_mcp_client()
        result = await mcp.call_tool("ollama_info")
        return result
    except Exception as e:
        logger.error(f"Error getting Ollama info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
