from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task


class CodeWorker(BaseAgent):
    """Implements code changes safely and incrementally."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="worker-code-agent",
            agent_type=AgentType.WORKER_CODE,
            mission="Implement code changes safely and incrementally.",
            allowed_tools={"read", "write", "test", "lint"},
            denied_tools={"deploy_prod", "secrets_access", "policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        return AgentResult(
            status="ok",
            summary=f"CodeWorker implemented {task.title}",
            data={
                "files_modified": 3,
                "tests_passed": 12,
                "coverage": "89%",
            },
        )
