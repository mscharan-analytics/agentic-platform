from __future__ import annotations

from dataclasses import dataclass, field

from agent_platform.agents.base import BaseAgent


@dataclass(slots=True)
class PolicyDecision:
    allow: bool
    reason_code: str
    obligations: list[str] = field(default_factory=list)


class PolicyEngine:
    def evaluate(self, agent: BaseAgent, action: str, resource: str = "") -> PolicyDecision:
        if action in agent.denied_tools:
            return PolicyDecision(allow=False, reason_code="POLICY_DENY_TOOL", obligations=[])
        if action not in agent.allowed_tools and action not in {"status", "plan", "analyze", "evaluate"}:
            return PolicyDecision(
                allow=False,
                reason_code="POLICY_NOT_IN_ALLOWED_SET",
                obligations=["Request elevated scope through Policy Agent"],
            )
        if action == "browser" and resource and not resource.startswith("https://"):
            return PolicyDecision(
                allow=False,
                reason_code="POLICY_INVALID_BROWSER_TARGET",
                obligations=["Use explicit https allowlisted domain"],
            )
        return PolicyDecision(allow=True, reason_code="POLICY_ALLOW", obligations=[])
