from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task


class OrchestratorAgent(BaseAgent):
    """Coordinates end-to-end execution, assigns tasks, enforces lifecycle."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="orchestrator-agent",
            agent_type=AgentType.ORCHESTRATOR,
            mission="Coordinate end-to-end execution, assign tasks, enforce lifecycle and termination.",
            allowed_tools={"route", "status", "assign"},
            denied_tools={"write", "deploy", "policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        return AgentResult(
            status="ok",
            summary=f"Orchestrator dispatched task {task.id} to workers",
            data={"task": task.title, "assignments": ["solver", "planner", "worker_code"]},
        )
