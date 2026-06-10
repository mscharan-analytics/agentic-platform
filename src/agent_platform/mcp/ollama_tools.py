"""MCP tools for Ollama model service management."""

from __future__ import annotations

import logging

from agent_platform.deployment_adapters.ollama import OllamaDeploymentAdapter

logger = logging.getLogger(__name__)


class OllamaTools:
    """MCP-registered tools for Ollama service introspection and management."""

    def __init__(self, adapter: OllamaDeploymentAdapter | None = None) -> None:
        self.adapter = adapter or OllamaDeploymentAdapter()

    @staticmethod
    async def list_available_models() -> dict[str, object]:
        """
        List all models available in the local Ollama instance.
        
        Returns dict with model names, sizes, and capabilities.
        """
        adapter = OllamaDeploymentAdapter()
        if not await adapter.initialize():
            return {
                "available": False,
                "message": "Ollama service not available",
                "models": [],
            }

        try:
            import httpx

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{adapter.config.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    models = [
                        {
                            "name": m.get("name"),
                            "size": m.get("size"),
                            "modified": m.get("modified_at"),
                        }
                        for m in data.get("models", [])
                    ]
                    return {
                        "available": True,
                        "count": len(models),
                        "models": models,
                    }
                else:
                    return {
                        "available": False,
                        "message": f"Ollama returned HTTP status {response.status_code}",
                        "models": [],
                    }
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return {"available": False, "error": str(e), "models": []}

    @staticmethod
    async def check_model_available(model_name: str) -> dict[str, object]:
        """Check if a specific model is available in Ollama."""
        adapter = OllamaDeploymentAdapter()
        if not await adapter.initialize():
            return {
                "model": model_name,
                "available": False,
                "reason": "Ollama service not available",
            }

        try:
            import httpx

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{adapter.config.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    for m in data.get("models", []):
                        if m.get("name") == model_name:
                            return {
                                "model": model_name,
                                "available": True,
                                "size": m.get("size"),
                                "modified": m.get("modified_at"),
                            }
        except Exception as e:
            logger.error(f"Error checking model: {e}")

        return {
            "model": model_name,
            "available": False,
            "reason": "Model not found or error during check",
        }

    @staticmethod
    async def get_ollama_version() -> dict[str, object]:
        """Get Ollama service version and configuration info."""
        adapter = OllamaDeploymentAdapter()
        if not await adapter.initialize():
            return {
                "available": False,
                "message": "Ollama service not available",
            }

        error_msg = "Ollama version check failed"
        try:
            import httpx

            async with httpx.AsyncClient(timeout=10.0) as client:
                # Ollama doesn't have a dedicated version endpoint, but we can use health
                response = await client.get(f"{adapter.config.base_url}/api/tags")
                if response.status_code == 200:
                    return {
                        "available": True,
                        "base_url": adapter.config.base_url,
                        "gpu_enabled": adapter.config.gpu_enabled,
                        "service_status": "healthy",
                    }
                else:
                    error_msg = f"HTTP status {response.status_code}"
        except Exception as e:
            logger.error(f"Error getting version: {e}")
            error_msg = str(e)

        return {"available": False, "error": error_msg}

    @staticmethod
    async def ollama_health_check() -> dict[str, object]:
        """Full Ollama service health check."""
        adapter = OllamaDeploymentAdapter()
        await adapter.initialize()
        return await adapter.health_check()
