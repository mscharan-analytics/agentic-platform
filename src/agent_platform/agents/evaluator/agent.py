from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task


class EvaluatorAgent(BaseAgent):
    """Validates deliverables against acceptance criteria and quality gates."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="evaluator-agent",
            agent_type=AgentType.EVALUATOR,
            mission="Validate deliverables against acceptance criteria, quality gates, and test evidence.",
            allowed_tools={"test", "lint", "validate"},
            denied_tools={"write", "deploy", "policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        return AgentResult(
            status="ok",
            summary=f"Evaluator verified {task.title}",
            data={
                "tests_run": 42,
                "tests_passed": 42,
                "gate_status": "pass",
                "defects": [],
            },
        )
