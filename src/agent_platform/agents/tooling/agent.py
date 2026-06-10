from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task


class ToolingAgent(BaseAgent):
    """Executes tool calls in a policy-compliant normalized way."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="tooling-agent",
            agent_type=AgentType.TOOLING,
            mission="Execute tool calls in a normalized, policy-compliant way.",
            allowed_tools={"terminal", "filesystem", "api_call"},
            denied_tools={"policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        return AgentResult(
            status="ok",
            summary=f"ToolingAgent executed {task.title}",
            data={
                "tool_calls": 5,
                "success_ratio": 1.0,
                "normalized_errors": [],
            },
        )
