from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class A2AMessageType(str, Enum):
    REQUEST = "request"
    DELEGATE = "delegate"
    ACKNOWLEDGE = "acknowledge"
    RESULT = "result"
    FAIL = "fail"
    CANCEL = "cancel"
    HEARTBEAT = "heartbeat"
    STATUS_QUERY = "status_query"
    STATUS_RESPONSE = "status_response"


class Priority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class AuthContext(BaseModel):
    actor_role: str
    auth_token_ref: str
    scopes: list[str] = Field(default_factory=list)


class A2AEnvelope(BaseModel):
    a2a_version: str = "1.0.0"
    message_type: A2AMessageType
    message_id: UUID = Field(default_factory=uuid4)
    correlation_id: UUID = Field(default_factory=uuid4)
    trace_id: UUID = Field(default_factory=uuid4)
    sender_agent_id: str
    receiver_agent_id: str
    priority: Priority = Priority.NORMAL
    timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    deadline_utc: datetime | None = None
    auth_context: AuthContext
    payload: dict[str, Any] = Field(default_factory=dict)
    attachments: dict[str, Any] = Field(default_factory=dict)
    policy_decision_ref: str
    signature: dict[str, Any] | None = None


class A2AState(str, Enum):
    CREATED = "created"
    SENT = "sent"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    WAITING_DEPENDENCY = "waiting_dependency"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMED_OUT = "timed_out"
