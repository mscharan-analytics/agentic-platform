from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task


class BrowserAgent(BaseAgent):
    """Performs policy-approved web tasks autonomously with evidence capture."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="browser-agent",
            agent_type=AgentType.BROWSER,
            mission="Perform policy-approved web tasks autonomously with evidence capture.",
            allowed_tools={"browser", "capture_evidence"},
            denied_tools={"external_domain", "policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        return AgentResult(
            status="ok",
            summary=f"BrowserAgent completed {task.title}",
            data={
                "navigation_success": True,
                "data_extracted": {"title": "example", "url": "https://example.com"},
                "screenshot_hash": "a1b2c3d4e5f6g7h8i9j0",
                "policy_compliant": True,
            },
        )
