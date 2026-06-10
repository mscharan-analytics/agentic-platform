from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task


class PlannerAgent(BaseAgent):
    """Builds dependency-aware execution plans with milestones."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="planner-agent",
            agent_type=AgentType.PLANNER,
            mission="Build dependency-aware execution plans with milestones and stop conditions.",
            allowed_tools={"plan", "split_tasks"},
            denied_tools={"deploy", "write", "policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        return AgentResult(
            status="ok",
            summary=f"Planner created execution DAG for {task.title}",
            data={
                "task_dag": [
                    {"id": "t-analyze", "deps": []},
                    {"id": "t-execute", "deps": ["t-analyze"]},
                    {"id": "t-validate", "deps": ["t-execute"]},
                ],
                "milestones": ["plan_review", "execution_gate", "evaluation"],
            },
        )
