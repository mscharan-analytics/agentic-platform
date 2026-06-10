"""Real-time event streaming via WebSocket."""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)
router = APIRouter()

# Global event store for tracking agent executions
_execution_events: dict[str, list[dict[str, Any]]] = {}
_event_subscribers: dict[str, set[WebSocket]] = {}


class EventStream:
    """Manages event streaming for agent executions."""

    @staticmethod
    def create_session() -> str:
        """Create a new execution session."""
        session_id = str(uuid.uuid4())
        _execution_events[session_id] = []
        _event_subscribers[session_id] = set()
        logger.info(f"Created execution session: {session_id}")
        return session_id

    @staticmethod
    def emit(session_id: str, event_type: str, data: dict[str, Any]) -> None:
        """Emit an event to all subscribers."""
        event = {
            "type": event_type,
            "timestamp": asyncio.get_event_loop().time(),
            "data": data,
        }
        if session_id in _execution_events:
            _execution_events[session_id].append(event)

    @staticmethod
    async def subscribe(session_id: str, websocket: WebSocket) -> None:
        """Subscribe a WebSocket to session events."""
        if session_id not in _event_subscribers:
            _event_subscribers[session_id] = set()
        _event_subscribers[session_id].add(websocket)

    @staticmethod
    async def broadcast(session_id: str, message: dict[str, Any]) -> None:
        """Broadcast a message to all subscribers."""
        if session_id in _event_subscribers:
            disconnected = set()
            for ws in _event_subscribers[session_id]:
                try:
                    await ws.send_json(message)
                except Exception as e:
                    logger.warning(f"WebSocket send failed: {e}")
                    disconnected.add(ws)
            _event_subscribers[session_id] -= disconnected

    @staticmethod
    def get_events(session_id: str) -> list[dict[str, Any]]:
        """Get all events for a session."""
        return _execution_events.get(session_id, [])

    @staticmethod
    def clear_session(session_id: str) -> None:
        """Clear a session."""
        _execution_events.pop(session_id, None)
        _event_subscribers.pop(session_id, None)


@router.websocket("/ws/logs/{session_id}")
async def websocket_logs(websocket: WebSocket, session_id: str) -> None:
    """WebSocket endpoint for real-time execution logs."""
    await websocket.accept()
    logger.info(f"WebSocket connected: {session_id}")

    try:
        await EventStream.subscribe(session_id, websocket)

        # Send existing events
        for event in EventStream.get_events(session_id):
            await websocket.send_json(event)

        # Keep connection open and listen for keep-alives
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
        if session_id in _event_subscribers:
            _event_subscribers[session_id].discard(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()


@router.get("/events/{session_id}")
async def get_execution_events(session_id: str) -> dict[str, object]:
    """Get all events for an execution session (polling fallback)."""
    events = EventStream.get_events(session_id)
    return {
        "session_id": session_id,
        "events": events,
        "count": len(events),
    }
