"""Model gateway management endpoints."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/providers")
async def get_model_providers() -> dict[str, object]:
    """List available model providers."""
    from agent_platform.model_gateway import ModelProvider

    providers = [p.value for p in ModelProvider]
    return {
        "providers": providers,
        "count": len(providers),
    }


@router.post("/invoke")
async def invoke_model(prompt: str, model: str = "llama2") -> dict[str, object]:
    """Invoke a model for inference."""
    try:
        from agent_platform.model_gateway import get_model_gateway

        gateway = get_model_gateway()
        response = await gateway.invoke(prompt, model)

        return {
            "model": model,
            "provider": response.provider.value,
            "response": response.content,
            "tokens_used": response.tokens_used,
        }
    except Exception as e:
        logger.error(f"Error invoking model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_model_status() -> dict[str, object]:
    """Get status of model providers."""
    from agent_platform.model_gateway import get_model_gateway

    gateway = get_model_gateway()
    ollama_available = gateway.ollama.is_available() if hasattr(gateway, "ollama") else False

    return {
        "ollama_available": ollama_available,
        "cloud_provider_configured": gateway.cloud_gateway is not None if hasattr(gateway, "cloud_gateway") else False,
    }
