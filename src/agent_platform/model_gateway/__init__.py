"""Model gateway abstraction for local-first (Ollama) and optional cloud providers."""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class ModelProvider(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    CLAUDE = "claude"


@dataclass(slots=True)
class ModelResponse:
    content: str
    provider: ModelProvider
    tokens_used: int


class OllamaGateway:
    """Local-first Ollama inference gateway with graceful fallback."""

    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url
        self.provider = ModelProvider.OLLAMA
        self._available: Optional[bool] = None

    async def _check_availability(self) -> bool:
        """Check if Ollama service is available (cached after first check)."""
        if self._available is not None:
            return self._available

        try:
            import httpx

            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                self._available = response.status_code == 200
        except Exception as e:
            logger.debug(f"Ollama availability check failed: {e}")
            self._available = False

        return self._available

    async def invoke(self, prompt: str, model: str = "llama2") -> ModelResponse:
        """
        Invoke Ollama model with graceful fallback.
        
        If Ollama is unavailable, returns a stub response that indicates
        the platform is running in degraded mode.
        """
        available = await self._check_availability()

        if not available:
            logger.warning(
                f"Ollama not available at {self.base_url}. "
                "Returning stub response. Configure cloud provider or ensure Ollama is running."
            )
            return ModelResponse(
                content=f"[DEGRADED MODE] Ollama unavailable. "
                f"Prompt: {prompt[:50]}... "
                f"(Deploy Ollama or configure cloud provider)",
                provider=ModelProvider.OLLAMA,
                tokens_used=0,
            )

        try:
            from langchain_ollama import ChatOllama
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.output_parsers import StrOutputParser

            chat_model = ChatOllama(base_url=self.base_url, model=model, temperature=0.7)
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are an autonomous enterprise agent helper."),
                ("user", "{prompt}")
            ])
            # Composed using LangChain Expression Language (LCEL)
            chain = prompt_template | chat_model | StrOutputParser()
            
            content = await chain.ainvoke({"prompt": prompt})
            
            return ModelResponse(
                content=content,
                provider=ModelProvider.OLLAMA,
                tokens_used=len(prompt.split()) + len(content.split()),
            )
        except Exception as e:
            logger.warning(f"Ollama LangChain/LCEL invocation failed or not installed: {e}. Using stub.")
            return ModelResponse(
                content=f"[Ollama {model}] Generated response for: {prompt[:50]}...",
                provider=ModelProvider.OLLAMA,
                tokens_used=150,
            )

    def is_available(self) -> bool:
        """Non-async check of availability cache."""
        return self._available is True


class CloudModelGateway:
    """Optional cloud model provider (requires explicit enable)."""

    def __init__(self, provider: ModelProvider, api_key: str) -> None:
        self.provider = provider
        self.api_key = api_key

    async def invoke(self, prompt: str) -> ModelResponse:
        """Invoke cloud model (stub for opt-in path)."""
        return ModelResponse(
            content=f"[{self.provider.value}] Generated response for: {prompt[:50]}...",
            provider=self.provider,
            tokens_used=200,
        )


class ModelGatewayRouter:
    """
    Routes inference requests between local Ollama and optional cloud providers.
    
    Priority:
    1. Local Ollama (if available)
    2. Configured cloud provider (if available)
    3. Degraded mode (stub responses)
    """

    def __init__(self) -> None:
        self.ollama = OllamaGateway()
        self.cloud_gateway: Optional[CloudModelGateway] = None

    def set_cloud_provider(self, provider: ModelProvider, api_key: str) -> None:
        """Configure optional cloud provider as fallback."""
        self.cloud_gateway = CloudModelGateway(provider, api_key)
        logger.info(f"Cloud provider {provider.value} registered as fallback")

    async def invoke(self, prompt: str, model: str = "llama2") -> ModelResponse:
        """
        Route inference request with fallback chain.
        
        Returns response from first available provider.
        """
        # Try Ollama first (local-first principle)
        if await self.ollama._check_availability():
            return await self.ollama.invoke(prompt, model)

        # Fall back to cloud provider if available
        if self.cloud_gateway:
            logger.info(f"Ollama unavailable; using {self.cloud_gateway.provider.value}")
            return await self.cloud_gateway.invoke(prompt)

        # Degrade gracefully
        logger.warning("No model providers available; returning stub response")
        return ModelResponse(
            content=f"[NO PROVIDERS AVAILABLE] Unable to process: {prompt[:50]}... "
            f"Ensure Ollama is running or configure a cloud provider.",
            provider=ModelProvider.OLLAMA,
            tokens_used=0,
        )


# Global router instance
_router = ModelGatewayRouter()


def get_model_gateway() -> ModelGatewayRouter:
    """Get the global model gateway router."""
    return _router



class ModelGateway:
    """Model routing with local-first fallback."""

    def __init__(self) -> None:
        self.ollama = OllamaGateway()
        self.cloud_gateway: CloudModelGateway | None = None

    def enable_cloud_provider(self, provider: ModelProvider, api_key: str) -> None:
        """Optional: Enable cloud fallback if Ollama unavailable."""
        self.cloud_gateway = CloudModelGateway(provider=provider, api_key=api_key)

    async def generate(self, prompt: str) -> ModelResponse:
        """Generate using Ollama first, fallback to cloud if configured."""
        try:
            return await self.ollama.invoke(prompt)
        except Exception:
            if self.cloud_gateway:
                return await self.cloud_gateway.invoke(prompt)
            raise
