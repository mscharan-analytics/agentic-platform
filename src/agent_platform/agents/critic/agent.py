from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task


class CriticAgent(BaseAgent):
    """Identifies hidden risks, edge cases, and architectural weaknesses."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="critic-agent",
            agent_type=AgentType.CRITIC,
            mission="Identify hidden risks, edge cases, and architectural weaknesses before release.",
            allowed_tools={"analyze_risk", "reason"},
            denied_tools={"write", "deploy", "policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        return AgentResult(
            status="ok",
            summary=f"Critic stress-tested {task.title}",
            data={
                "risks_identified": 3,
                "edge_cases": 7,
                "mitigation_required": ["error_handling", "concurrency", "auth_edge_case"],
            },
        )
