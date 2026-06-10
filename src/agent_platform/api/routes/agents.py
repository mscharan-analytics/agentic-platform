"""Agent management endpoints."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from fastapi import APIRouter, HTTPException

from agent_platform.api.routes.events import EventStream

logger = logging.getLogger(__name__)
router = APIRouter()

# Track running executions
_running_executions: dict[str, dict[str, Any]] = {}


@router.get("/list")
async def list_agents() -> dict[str, object]:
    """List all available agents in the catalog."""
    from agent_platform.agents.catalog import AgentCatalog

    try:
        catalog = AgentCatalog()
        agents = catalog.list_agents()
        return {
            "agents": [
                {
                    "name": a.agent_id,
                    "description": a.mission,
                    "type": a.agent_type.value,
                }
                for a in agents
            ],
            "count": len(agents),
        }
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_name}")
async def get_agent_info(agent_name: str) -> dict[str, object]:
    """Get detailed information about a specific agent."""
    from agent_platform.agents.catalog import AgentCatalog

    try:
        catalog = AgentCatalog()
        agent = catalog.get_agent(agent_name)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")

        return {
            "name": agent.agent_id,
            "description": agent.mission,
            "type": agent.agent_type.value,
            "allowed_tools": sorted(agent.allowed_tools),
            "denied_tools": sorted(agent.denied_tools),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent {agent_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_name}/deploy")
async def deploy_agent(agent_name: str, payload: dict[str, Any] | None = None) -> dict[str, object]:
    """Deploy and execute an agent."""
    from agent_platform.agents.catalog import AgentCatalog

    try:
        logger.info(f"Deploying agent {agent_name}")
        payload = payload or {}

        # Create execution session
        session_id = EventStream.create_session()

        # Verify agent exists
        catalog = AgentCatalog()
        agent = catalog.get_agent(agent_name)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")

        # Track execution
        _running_executions[session_id] = {
            "agent": agent_name,
            "status": "running",
            "payload": payload,
        }

        # Emit deployment event
        await EventStream.broadcast(
            session_id,
            {
                "type": "deployment_started",
                "data": {
                    "agent": agent_name,
                    "session_id": session_id,
                },
            },
        )

        # Simulate async execution (in real implementation, queue this task)
        asyncio.create_task(_execute_agent_async(session_id, agent_name, payload))

        return {
            "agent": agent_name,
            "session_id": session_id,
            "status": "deployed",
            "message": f"Agent {agent_name} deployment started",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deploying agent {agent_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_name}/execution/{session_id}")
async def get_execution_status(agent_name: str, session_id: str) -> dict[str, object]:
    """Get status of a running agent execution."""
    if session_id not in _running_executions:
        raise HTTPException(status_code=404, detail=f"Execution {session_id} not found")

    execution = _running_executions[session_id]
    events = EventStream.get_events(session_id)

    return {
        "agent": agent_name,
        "session_id": session_id,
        "status": execution["status"],
        "events": events,
        "event_count": len(events),
    }


@router.post("/{agent_name}/execution/{session_id}/cancel")
async def cancel_execution(agent_name: str, session_id: str) -> dict[str, object]:
    """Cancel a running agent execution."""
    if session_id not in _running_executions:
        raise HTTPException(status_code=404, detail=f"Execution {session_id} not found")

    execution = _running_executions[session_id]
    execution["status"] = "cancelled"

    await EventStream.broadcast(
        session_id,
        {
            "type": "execution_cancelled",
            "data": {"session_id": session_id},
        },
    )

    return {
        "session_id": session_id,
        "status": "cancelled",
    }


async def _execute_agent_async(session_id: str, agent_name: str, payload: dict[str, Any]) -> None:
    """Execute agent asynchronously and emit events."""
    try:
        await EventStream.broadcast(
            session_id,
            {
                "type": "execution_progress",
                "data": {
                    "message": f"Initializing {agent_name}...",
                    "progress": 10,
                },
            },
        )

        # Simulate work
        await asyncio.sleep(1)

        await EventStream.broadcast(
            session_id,
            {
                "type": "execution_progress",
                "data": {
                    "message": f"Running {agent_name}...",
                    "progress": 50,
                },
            },
        )

        await asyncio.sleep(1)

        await EventStream.broadcast(
            session_id,
            {
                "type": "execution_progress",
                "data": {
                    "message": f"{agent_name} complete",
                    "progress": 100,
                },
            },
        )

        if session_id in _running_executions:
            _running_executions[session_id]["status"] = "completed"

        await EventStream.broadcast(
            session_id,
            {
                "type": "execution_completed",
                "data": {
                    "agent": agent_name,
                    "result": "Execution successful",
                },
            },
        )
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        if session_id in _running_executions:
            _running_executions[session_id]["status"] = "failed"

        await EventStream.broadcast(
            session_id,
            {
                "type": "execution_failed",
                "data": {
                    "error": str(e),
                },
            },
        )

