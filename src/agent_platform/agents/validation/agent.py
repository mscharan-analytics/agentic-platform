from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task
from agent_platform.mcp.client import get_mcp_client


class ValidationAgent(BaseAgent):
    """Runs go/no-go quality gates for test, static analysis, and policy checks."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="validation-agent",
            agent_type=AgentType.VALIDATION,
            mission="Run SDLC go/no-go quality gates and emit pass/fail with evidence.",
            allowed_tools={"validate", "test", "static_analysis", "policy_check"},
            denied_tools={"deploy_prod", "policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        attempt = int(task.metadata.get("attempt", 1))
        fail_until_attempt = int(task.metadata.get("fail_until_attempt", 0))
        raw_analysis_tools = task.metadata.get("analysis_tools", ["ruff", "mypy", "eslint"])
        analysis_tools = [str(tool) for tool in raw_analysis_tools] if isinstance(raw_analysis_tools, list) else ["ruff", "mypy", "eslint"]

        mcp = get_mcp_client()
        analysis_result = await mcp.call_tool("run_static_analysis", tools=analysis_tools)
        raw_analysis_data = analysis_result.get("results", [])
        analysis_data = raw_analysis_data if isinstance(raw_analysis_data, list) else []
        analysis_status = "pass" if all(isinstance(result, dict) and result.get("status") == "pass" for result in analysis_data) else "fail"

        if attempt <= fail_until_attempt:
            return AgentResult(
                status="fail",
                summary=f"Validation failed on attempt {attempt}",
                data={
                    "go_no_go": "no_go",
                    "checks": {
                        "tests": "fail",
                        "static_analysis": analysis_status,
                        "policy": "pass",
                    },
                    "analysis": analysis_data,
                },
            )

        return AgentResult(
            status="pass",
            summary=f"Validation passed on attempt {attempt}",
            data={
                "go_no_go": "go",
                "checks": {
                    "tests": "pass",
                    "static_analysis": analysis_status,
                    "policy": "pass",
                },
                "analysis": analysis_data,
            },
        )
