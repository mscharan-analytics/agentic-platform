from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from agent_platform.agents.base import AgentType, BaseAgent, Task
from agent_platform.contracts.acp import (
    ACPEnvelope,
    ACPObservability,
    ACPPayload,
    ACPPolicyContext,
    ACPProvenance,
    compute_integrity_hash,
)
from agent_platform.orchestration.hooks import HookEvent, HookManager, HookType
from agent_platform.policy.engine import PolicyEngine


class AutonomousRunner:
    def __init__(self, registry: dict[AgentType, BaseAgent], hooks: HookManager, policy: PolicyEngine) -> None:
        self.registry = registry
        self.hooks = hooks
        self.policy = policy

    def _build_context(self, sender: str, recipient: str, objective: str, trace_id: str) -> ACPEnvelope:
        payload = ACPPayload(
            objective_summary=objective,
            constraints=["enterprise_policy", "audit_required"],
            assumptions=["local-first model routing"],
            required_actions=["plan", "execute", "evaluate"],
            completion_criteria=["task_complete", "policy_compliant"],
        )
        return ACPEnvelope(
            sender_agent_id=sender,
            recipient_agent_id=recipient,
            integrity_hash=compute_integrity_hash(payload),
            provenance=ACPProvenance(
                source_refs=["goal_request"],
                collected_by_agent=sender,
                collected_at_utc=datetime.now(timezone.utc),
                confidence_score=0.9,
            ),
            context_payload=payload,
            policy_context=ACPPolicyContext(
                rbac_scope=["agent:run"],
                allowed_tools=["plan", "read", "test", "evaluate"],
                denied_tools=["deploy_prod"],
            ),
            observability=ACPObservability(span_id=trace_id, metric_tags={"runner": "autonomous"}),
        )

    async def run(self, goal: str, max_steps: int = 8) -> dict[str, object]:
        trace_id = str(uuid4())
        self.hooks.emit(HookEvent(HookType.PRE_TASK, trace_id, {"goal": goal}))

        solver = self.registry[AgentType.SOLVER]
        planner = self.registry[AgentType.PLANNER]
        evaluator = self.registry[AgentType.EVALUATOR]
        worker = self.registry[AgentType.WORKER_CODE]

        plan_task = Task(id="t-solve", title="Solve goal", objective=goal)
        plan_ctx = self._build_context("orchestrator-agent", solver.agent_id, goal, trace_id)
        self.hooks.emit(HookEvent(HookType.PRE_AGENT_STEP, trace_id, {"agent": solver.agent_id}))
        solve_result = await solver.run(plan_task, plan_ctx)
        self.hooks.emit(HookEvent(HookType.POST_AGENT_STEP, trace_id, {"result": solve_result.summary}))

        planning_task = Task(id="t-plan", title="Plan execution", objective=goal)
        planning_ctx = self._build_context(solver.agent_id, planner.agent_id, goal, trace_id)
        self.hooks.emit(HookEvent(HookType.PRE_AGENT_STEP, trace_id, {"agent": planner.agent_id}))
        plan_result = await planner.run(planning_task, planning_ctx)
        self.hooks.emit(HookEvent(HookType.POST_AGENT_STEP, trace_id, {"result": plan_result.summary}))

        step_results: list[str] = []
        for index in range(max_steps):
            action = "write" if index % 2 == 0 else "test"
            decision = self.policy.evaluate(worker, action=action)
            if not decision.allow:
                self.hooks.emit(
                    HookEvent(
                        HookType.ON_ERROR,
                        trace_id,
                        {
                            "agent": worker.agent_id,
                            "step": index,
                            "reason": decision.reason_code,
                        },
                    )
                )
                break

            task = Task(id=f"t-work-{index}", title=f"Execute step {index}", objective=goal)
            ctx = self._build_context(planner.agent_id, worker.agent_id, goal, trace_id)
            self.hooks.emit(HookEvent(HookType.PRE_AGENT_STEP, trace_id, {"agent": worker.agent_id, "step": index}))
            result = await worker.run(task, ctx)
            step_results.append(result.summary)
            self.hooks.emit(HookEvent(HookType.POST_AGENT_STEP, trace_id, {"step": index, "result": result.summary}))

            if index >= 2:
                break

        eval_task = Task(id="t-eval", title="Evaluate run", objective=goal)
        eval_ctx = self._build_context(worker.agent_id, evaluator.agent_id, goal, trace_id)
        eval_result = await evaluator.run(eval_task, eval_ctx)

        self.hooks.emit(HookEvent(HookType.POST_TASK, trace_id, {"evaluation": eval_result.summary}))

        return {
            "trace_id": trace_id,
            "solver": solve_result.summary,
            "planner": plan_result.summary,
            "steps": step_results,
            "evaluation": eval_result.summary,
            "audit_events": len(self.hooks.audit_log),
        }

    async def run_sdlc_pipeline(
        self,
        goal: str,
        target_env: str = "dev",
        ci_target: str = "github_actions",
        max_validation_retries: int = 2,
        fail_until_attempt: int = 0,
    ) -> dict[str, object]:
        """Run an SDLC-oriented multi-agent loop with validation go/no-go gates."""
        trace_id = str(uuid4())
        self.hooks.emit(HookEvent(HookType.PRE_TASK, trace_id, {"goal": goal, "mode": "sdlc"}))

        scheduler = self.registry[AgentType.SCHEDULER]
        solver = self.registry[AgentType.SOLVER]
        planner = self.registry[AgentType.PLANNER]
        worker_code = self.registry[AgentType.WORKER_CODE]
        worker_integration = self.registry[AgentType.WORKER_INTEGRATION]
        validation = self.registry[AgentType.VALIDATION]
        evaluator = self.registry[AgentType.EVALUATOR]
        deployment = self.registry[AgentType.DEPLOYMENT]

        sdlc_stages: list[dict[str, object]] = []

        schedule_task = Task(
            id="sdlc-schedule",
            title="Schedule pipeline",
            objective=goal,
            metadata={"target_env": target_env},
        )
        schedule_ctx = self._build_context("orchestrator-agent", scheduler.agent_id, goal, trace_id)
        schedule_result = await scheduler.run(schedule_task, schedule_ctx)
        sdlc_stages.append({"stage": "schedule", "status": schedule_result.status, "summary": schedule_result.summary})

        requirements_task = Task(
            id="sdlc-requirements",
            title="Requirements intake",
            objective=goal,
            metadata={"sources": ["figma", "lucid", "jira"]},
        )
        req_ctx = self._build_context("orchestrator-agent", solver.agent_id, goal, trace_id)
        req_result = await solver.run(requirements_task, req_ctx)
        sdlc_stages.append({"stage": "requirements_intake", "status": req_result.status, "summary": req_result.summary})

        conversion_task = Task(id="sdlc-task-conversion", title="Convert stories to tasks", objective=goal)
        conversion_ctx = self._build_context(solver.agent_id, planner.agent_id, goal, trace_id)
        conversion_result = await planner.run(conversion_task, conversion_ctx)
        sdlc_stages.append({"stage": "task_conversion", "status": conversion_result.status, "summary": conversion_result.summary})

        code_task = Task(id="sdlc-codegen", title="Generate code and tests", objective=goal)
        code_ctx = self._build_context(planner.agent_id, worker_code.agent_id, goal, trace_id)
        code_result = await worker_code.run(code_task, code_ctx)
        sdlc_stages.append({"stage": "code_generation", "status": code_result.status, "summary": code_result.summary})

        build_task = Task(id="sdlc-build", title="Build and package", objective=goal)
        build_ctx = self._build_context(worker_code.agent_id, worker_integration.agent_id, goal, trace_id)
        build_result = await worker_integration.run(build_task, build_ctx)
        sdlc_stages.append({"stage": "build", "status": build_result.status, "summary": build_result.summary})

        validation_attempt = 1
        validation_summary = ""
        validation_passed = False
        while validation_attempt <= (max_validation_retries + 1):
            validation_task = Task(
                id=f"sdlc-validation-{validation_attempt}",
                title="Validation go/no-go",
                objective=goal,
                metadata={
                    "attempt": validation_attempt,
                    "fail_until_attempt": fail_until_attempt,
                    "analysis_tools": ["ruff", "mypy", "eslint"],
                },
            )
            validation_ctx = self._build_context(worker_integration.agent_id, validation.agent_id, goal, trace_id)
            validation_result = await validation.run(validation_task, validation_ctx)
            validation_summary = validation_result.summary
            sdlc_stages.append(
                {
                    "stage": "validation",
                    "attempt": validation_attempt,
                    "status": validation_result.status,
                    "summary": validation_result.summary,
                    "decision": validation_result.data.get("go_no_go", "no_go"),
                }
            )

            if validation_result.status == "pass" and validation_result.data.get("go_no_go") == "go":
                validation_passed = True
                break

            rework_task = Task(
                id=f"sdlc-rework-{validation_attempt}",
                title="Rework after validation failure",
                objective=goal,
                metadata={"attempt": validation_attempt},
            )
            rework_ctx = self._build_context(validation.agent_id, worker_code.agent_id, goal, trace_id)
            rework_result = await worker_code.run(rework_task, rework_ctx)
            sdlc_stages.append(
                {
                    "stage": "rework",
                    "attempt": validation_attempt,
                    "status": rework_result.status,
                    "summary": rework_result.summary,
                }
            )
            validation_attempt += 1

        if validation_passed:
            deploy_task = Task(
                id="sdlc-deploy",
                title="Deploy through CI/CD",
                objective=goal,
                metadata={"target_env": target_env, "ci_target": ci_target},
            )
            deploy_ctx = self._build_context(validation.agent_id, deployment.agent_id, goal, trace_id)
            deploy_result = await deployment.run(deploy_task, deploy_ctx)
            sdlc_stages.append({"stage": "deploy", "status": deploy_result.status, "summary": deploy_result.summary})

            observability_task = Task(id="sdlc-observability", title="Observe health/metrics/logs", objective=goal)
            observability_ctx = self._build_context(deployment.agent_id, evaluator.agent_id, goal, trace_id)
            observability_result = await evaluator.run(observability_task, observability_ctx)
            sdlc_stages.append(
                {
                    "stage": "observability",
                    "status": observability_result.status,
                    "summary": observability_result.summary,
                }
            )
            overall_status = "completed"
        else:
            overall_status = "blocked_no_go"

        self.hooks.emit(
            HookEvent(
                HookType.POST_TASK,
                trace_id,
                {
                    "mode": "sdlc",
                    "status": overall_status,
                    "validation": validation_summary,
                },
            )
        )

        return {
            "trace_id": trace_id,
            "goal": goal,
            "target_env": target_env,
            "ci_target": ci_target,
            "status": overall_status,
            "stages": sdlc_stages,
            "validation_attempts": validation_attempt,
            "audit_events": len(self.hooks.audit_log),
        }
