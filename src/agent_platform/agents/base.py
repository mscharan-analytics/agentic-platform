from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from agent_platform.contracts.acp import ACPEnvelope


class AgentType(str, Enum):
    ORCHESTRATOR = "orchestrator"
    SOLVER = "solver"
    PLANNER = "planner"
    SCHEDULER = "scheduler"
    WORKER_CODE = "worker_code"
    WORKER_INTEGRATION = "worker_integration"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"
    TOOLING = "tooling"
    CONTEXT = "context"
    POLICY = "policy"
    EVALUATOR = "evaluator"
    CRITIC = "critic"
    BROWSER = "browser"
    RECOVERY = "recovery"


@dataclass(slots=True)
class Task:
    id: str
    title: str
    objective: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AgentResult:
    status: str
    summary: str
    data: dict[str, Any] = field(default_factory=dict)


class BaseAgent:
    def __init__(
        self,
        agent_id: str,
        agent_type: AgentType,
        mission: str,
        allowed_tools: set[str],
        denied_tools: set[str],
    ) -> None:
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.mission = mission
        self.allowed_tools = allowed_tools
        self.denied_tools = denied_tools

    async def run(self, task: Task, context: ACPEnvelope | None = None) -> AgentResult:
        raise NotImplementedError("Agents must implement run()")
