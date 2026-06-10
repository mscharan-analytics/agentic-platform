from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task


class SchedulerAgent(BaseAgent):
    """Coordinates task timing for build/test/release orchestration."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="scheduler-agent",
            agent_type=AgentType.SCHEDULER,
            mission="Schedule SDLC stages and coordinate CI/CD trigger timing.",
            allowed_tools={"schedule", "trigger_ci", "trigger_release"},
            denied_tools={"policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        env = str(task.metadata.get("target_env", "dev"))
        return AgentResult(
            status="ok",
            summary=f"Scheduler planned SDLC execution for {env}",
            data={
                "target_env": env,
                "timeline": [
                    "requirements_intake",
                    "task_conversion",
                    "code_generation",
                    "build",
                    "validation",
                    "deployment",
                    "observability",
                ],
            },
        )
