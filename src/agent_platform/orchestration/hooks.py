from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any


class HookType(str, Enum):
    PRE_TASK = "pre_task"
    PRE_AGENT_STEP = "pre_agent_step"
    PRE_TOOL_CALL = "pre_tool_call"
    POST_TOOL_CALL = "post_tool_call"
    POST_AGENT_STEP = "post_agent_step"
    POST_TASK = "post_task"
    ON_ERROR = "on_error"


@dataclass(slots=True)
class HookEvent:
    hook_type: HookType
    trace_id: str
    payload: dict[str, Any]


HookCallback = Callable[[HookEvent], None]


class HookManager:
    def __init__(self) -> None:
        self._handlers: dict[HookType, list[HookCallback]] = {hook: [] for hook in HookType}
        self.audit_log: list[HookEvent] = []

    def register(self, hook_type: HookType, callback: HookCallback) -> None:
        self._handlers[hook_type].append(callback)

    def emit(self, event: HookEvent) -> None:
        self.audit_log.append(event)
        for callback in self._handlers[event.hook_type]:
            callback(event)
