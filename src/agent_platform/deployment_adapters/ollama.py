"""Ollama deployment adapter for local model service orchestration."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class OllamaConfig:
    """Ollama deployment configuration."""

    base_url: str = "http://localhost:11434"
    models: list[str] | None = None
    keep_alive: str = "30m"
    memory_limit: str | None = None
    gpu_enabled: bool = True


class OllamaDeploymentAdapter:
    """
    Manages Ollama service lifecycle for local-first deployments.
    
    Responsibilities:
    - Health checks and readiness probes
    - Model inventory and pulling
    - Configuration validation
    - Graceful degradation if Ollama unavailable
    """

    def __init__(self, config: OllamaConfig | None = None) -> None:
        self.config = config or self._from_env()
        self._client: Any = None
        self._available = False

    @staticmethod
    def _from_env() -> OllamaConfig:
        """Load Ollama config from environment variables."""
        return OllamaConfig(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            models=os.getenv("OLLAMA_MODELS", "llama2").split(","),
            keep_alive=os.getenv("OLLAMA_KEEP_ALIVE", "30m"),
            memory_limit=os.getenv("OLLAMA_MEMORY_LIMIT"),
            gpu_enabled=os.getenv("OLLAMA_GPU_ENABLED", "true").lower() == "true",
        )

    async def initialize(self) -> bool:
        """
        Initialize Ollama service connection.
        
        Returns True if Ollama is available, False otherwise (graceful fallback).
        """
        try:
            import httpx

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.config.base_url}/api/tags")
                self._available = response.status_code == 200
                if self._available:
                    logger.info(f"✓ Ollama service available at {self.config.base_url}")
                else:
                    logger.warning(
                        f"✗ Ollama service unavailable ({response.status_code}). "
                        f"Platform will use fallback LLM routing."
                    )
        except Exception as e:
            logger.warning(f"✗ Cannot connect to Ollama: {e}. Running in degraded mode.")
            self._available = False
        return self._available

    async def pull_models(self) -> dict[str, bool]:
        """
        Pull required models into local Ollama instance.
        
        Returns dict mapping model name -> pull success.
        """
        if not self._available:
            logger.info("Ollama not available; skipping model pulls.")
            return {}

        try:
            import httpx

            results = {}
            async with httpx.AsyncClient(timeout=300.0) as client:  # Models can take time to pull
                for model in self.config.models or ["llama2"]:
                    try:
                        logger.info(f"Pulling model: {model}")
                        response = await client.post(
                            f"{self.config.base_url}/api/pull",
                            json={"name": model},
                        )
                        results[model] = response.status_code == 200
                        if results[model]:
                            logger.info(f"✓ Successfully pulled {model}")
                        else:
                            logger.warning(f"✗ Failed to pull {model} (HTTP {response.status_code})")
                    except Exception as e:
                        logger.error(f"✗ Error pulling {model}: {e}")
                        results[model] = False
            return results
        except ImportError:
            logger.error("httpx not installed; cannot pull models. Install with: pip install ollama[deployment]")
            return {}

    async def health_check(self) -> dict[str, object]:
        """
        Get Ollama service health and loaded model status.
        
        Returns dict with service_status, models_loaded, etc.
        """
        if not self._available:
            return {
                "service_available": False,
                "message": "Ollama not initialized or unreachable",
            }

        error_msg = "Ollama returned non-200 status code"
        try:
            import httpx

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.config.base_url}/api/tags")
                if response.status_code == 200:
                    models_data = response.json()
                    return {
                        "service_available": True,
                        "models_loaded": len(models_data.get("models", [])),
                        "models": [m.get("name", "unknown") for m in models_data.get("models", [])],
                    }
                else:
                    error_msg = f"HTTP status {response.status_code}"
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            error_msg = str(e)

        return {"service_available": False, "error": error_msg}

    def is_available(self) -> bool:
        """Check if Ollama service is available."""
        return self._available

    async def configure_resource_limits(self) -> bool:
        """
        Configure memory/resource limits for Ollama if specified.
        
        Note: This is environment-dependent and may not work in all contexts.
        """
        if not self.config.memory_limit or not self._available:
            return False

        logger.info(f"Setting Ollama memory limit to {self.config.memory_limit}")
        # Resource limit configuration would happen via environment or systemd
        # For Docker, this is handled via docker-compose resource constraints
        return True
