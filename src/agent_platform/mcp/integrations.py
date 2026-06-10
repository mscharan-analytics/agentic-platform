"""MCP tools for external integrations (Jira, Figma, Lucid, Ollama)."""

from __future__ import annotations

from agent_platform.integrations import FigmaConnector, JiraConnector, LucidConnector
from agent_platform.mcp.ollama_tools import OllamaTools


class IntegrationTools:
    """MCP-registered tools for requirements intake and model service management."""

    @staticmethod
    async def fetch_jira_stories(project_key: str, max_items: int = 20) -> dict[str, object]:
        """Fetch stories from Jira project."""
        jira = JiraConnector(base_url="https://example.atlassian.net", project_key=project_key)
        stories = await jira.fetch_stories(max_items=max_items)
        return {
            "project_key": project_key,
            "stories": [
                {"key": s.key, "summary": s.summary, "acceptance_criteria": s.acceptance_criteria}
                for s in stories
            ],
        }

    @staticmethod
    async def fetch_figma_spec(file_key: str) -> dict[str, object]:
        """Fetch design spec from Figma file."""
        figma = FigmaConnector()
        spec = await figma.fetch_spec(file_key)
        return {
            "file_key": spec.file_key,
            "screen_count": spec.screen_count,
            "notes": spec.notes,
        }

    @staticmethod
    async def fetch_lucid_diagram(doc_id: str) -> dict[str, object]:
        """Fetch architecture from Lucid diagram."""
        lucid = LucidConnector()
        diagram = await lucid.fetch_diagram(doc_id)
        return {
            "doc_id": diagram.doc_id,
            "components": diagram.components,
        }

    # Ollama model service tools
    @staticmethod
    async def ollama_list_models() -> dict[str, object]:
        """List all available models in the local Ollama instance."""
        return await OllamaTools.list_available_models()

    @staticmethod
    async def ollama_check_model(model_name: str) -> dict[str, object]:
        """Check if a specific Ollama model is available."""
        return await OllamaTools.check_model_available(model_name)

    @staticmethod
    async def ollama_health() -> dict[str, object]:
        """Check Ollama service health."""
        return await OllamaTools.ollama_health_check()

    @staticmethod
    async def ollama_info() -> dict[str, object]:
        """Get Ollama service version and configuration."""
        return await OllamaTools.get_ollama_version()

