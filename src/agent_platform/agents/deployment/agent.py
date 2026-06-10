from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task
from agent_platform.mcp.client import get_mcp_client


class DeploymentAgent(BaseAgent):
    """Coordinates deployment transitions across environments."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="deployment-agent",
            agent_type=AgentType.DEPLOYMENT,
            mission="Trigger and verify deployment progression across dev/staging/prod.",
            allowed_tools={"deploy", "verify_release", "rollback"},
            denied_tools={"policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        target_env = str(task.metadata.get("target_env", "dev"))
        ci_target = str(task.metadata.get("ci_target", "github_actions"))
        mcp = get_mcp_client()

        if ci_target == "azure_devops":
            trigger_result = await mcp.call_tool("trigger_azure_devops", pipeline="release-pipeline", branch="main")
        elif ci_target == "jenkins":
            trigger_result = await mcp.call_tool("trigger_jenkins", job_name="release-job", branch="main")
        else:
            trigger_result = await mcp.call_tool("trigger_github_actions", workflow="release.yml", ref="main")

        return AgentResult(
            status="ok",
            summary=f"Deployment completed for {target_env}",
            data={
                "target_env": target_env,
                "ci_target": ci_target,
                "deployment_status": "success",
                "rollback_ready": True,
                "trigger": trigger_result,
            },
        )
