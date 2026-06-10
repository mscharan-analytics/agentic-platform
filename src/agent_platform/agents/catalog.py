from __future__ import annotations

from agent_platform.agents.base import AgentType, BaseAgent
from agent_platform.agents.browser import BrowserAgent
from agent_platform.agents.context_manager import ContextAgent
from agent_platform.agents.critic import CriticAgent
from agent_platform.agents.deployment import DeploymentAgent
from agent_platform.agents.evaluator import EvaluatorAgent
from agent_platform.agents.orchestrator import OrchestratorAgent
from agent_platform.agents.planner import PlannerAgent
from agent_platform.agents.recovery import RecoveryAgent
from agent_platform.agents.scheduler import SchedulerAgent
from agent_platform.agents.solver import SolverAgent
from agent_platform.agents.tooling import ToolingAgent
from agent_platform.agents.validation import ValidationAgent
from agent_platform.agents.workers import CodeWorker, IntegrationWorker


def default_agent_registry() -> dict[AgentType, BaseAgent]:
    """Create default registry of all 12 enterprise agents."""
    return {
        AgentType.ORCHESTRATOR: OrchestratorAgent(),
        AgentType.SOLVER: SolverAgent(),
        AgentType.PLANNER: PlannerAgent(),
        AgentType.SCHEDULER: SchedulerAgent(),
        AgentType.WORKER_CODE: CodeWorker(),
        AgentType.WORKER_INTEGRATION: IntegrationWorker(),
        AgentType.VALIDATION: ValidationAgent(),
        AgentType.DEPLOYMENT: DeploymentAgent(),
        AgentType.TOOLING: ToolingAgent(),
        AgentType.CONTEXT: ContextAgent(),
        AgentType.EVALUATOR: EvaluatorAgent(),
        AgentType.CRITIC: CriticAgent(),
        AgentType.BROWSER: BrowserAgent(),
        AgentType.RECOVERY: RecoveryAgent(),
    }


class AgentCatalog:
    """Simple in-memory catalog for API and runtime use."""

    def __init__(self) -> None:
        self._registry = default_agent_registry()

    def list_agents(self) -> list[BaseAgent]:
        """Return all registered agent instances."""
        return list(self._registry.values())

    def get_agent(self, agent_name: str) -> BaseAgent | None:
        """Get an agent by id or type value."""
        for agent_type, agent in self._registry.items():
            if agent.agent_id == agent_name or agent_type.value == agent_name:
                return agent
        return None

