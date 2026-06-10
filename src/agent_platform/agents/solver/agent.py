import os

from agent_platform.agents.base import AgentResult, AgentType, BaseAgent, Task
from agent_platform.mcp.client import get_mcp_client


class SolverAgent(BaseAgent):
    """Converts ambiguous objectives into solvable problem statements."""

    def __init__(self) -> None:
        super().__init__(
            agent_id="solver-agent",
            agent_type=AgentType.SOLVER,
            mission="Convert ambiguous objectives into solvable problem statements and target outcomes.",
            allowed_tools={"analyze", "reason"},
            denied_tools={"write", "deploy", "policy_override"},
        )

    async def run(self, task: Task, context=None) -> AgentResult:  # type: ignore[override]
        sources = task.metadata.get("sources", [])
        intake_data: dict[str, object] = {}
        mcp = get_mcp_client()

        if isinstance(sources, list) and sources:
            if "jira" in sources:
                jira_result = await mcp.call_tool(
                    "fetch_jira_stories",
                    project_key=os.getenv("JIRA_PROJECT_KEY", "DEMO"),
                    max_items=10,
                )
                intake_data["jira_stories"] = jira_result.get("stories", [])

            if "figma" in sources:
                figma_file_key = str(task.metadata.get("figma_file_key", os.getenv("FIGMA_FILE_KEY", "demo-file")))
                figma_result = await mcp.call_tool("fetch_figma_spec", file_key=figma_file_key)
                intake_data["figma"] = figma_result

            if "lucid" in sources:
                lucid_doc_id = str(task.metadata.get("lucid_doc_id", os.getenv("LUCID_DOC_ID", "demo-doc")))
                lucid_result = await mcp.call_tool("fetch_lucid_diagram", doc_id=lucid_doc_id)
                intake_data["lucid"] = lucid_result

        return AgentResult(
            status="ok",
            summary=f"Solver decomposed objective: {task.objective}",
            data={
                "problem_statement": task.objective,
                "constraints": ["enterprise_policy", "audit_required"],
                "success_criteria": ["policy_compliant", "auditable"],
                "requirements_intake": intake_data,
            },
        )
