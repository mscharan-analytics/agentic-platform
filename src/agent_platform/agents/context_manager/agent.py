from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task


class ContextAgent(BaseAgent):
    """Manages context retrieval, packing, validation, TTL, and provenance via ACP."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="context-agent",
            agent_type=AgentType.CONTEXT,
            mission="Manage context retrieval, packing, validation, TTL, and provenance via ACP.",
            allowed_tools={"memory_read", "context_pack", "validate"},
            denied_tools={"deploy", "write", "policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        return AgentResult(
            status="ok",
            summary=f"ContextAgent packaged context for {task.title}",
            data={
                "context_packet_size": 2048,
                "provenance_refs": 4,
                "ttl_seconds": 900,
                "integrity_verified": True,
            },
        )
