from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from json import dumps
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class Classification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class ACPProvenance(BaseModel):
    source_refs: list[str] = Field(default_factory=list)
    collected_by_agent: str
    collected_at_utc: datetime
    confidence_score: float = Field(ge=0.0, le=1.0)


class ACPPayload(BaseModel):
    objective_summary: str
    constraints: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    required_actions: list[str] = Field(default_factory=list)
    completion_criteria: list[str] = Field(default_factory=list)


class ACPPolicyContext(BaseModel):
    rbac_scope: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    denied_tools: list[str] = Field(default_factory=list)
    approval_requirements: list[str] = Field(default_factory=list)


class ACPObservability(BaseModel):
    span_id: str
    metric_tags: dict[str, str] = Field(default_factory=dict)


class ACPEnvelope(BaseModel):
    protocol_name: str = "ACP"
    protocol_version: str = "1.0.0"
    message_id: UUID = Field(default_factory=uuid4)
    correlation_id: UUID = Field(default_factory=uuid4)
    trace_id: UUID = Field(default_factory=uuid4)
    parent_message_id: UUID | None = None
    sender_agent_id: str
    recipient_agent_id: str
    timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    ttl_seconds: int = Field(default=900, gt=0)
    classification: Classification = Classification.INTERNAL
    integrity_hash: str
    provenance: ACPProvenance
    context_payload: ACPPayload
    policy_context: ACPPolicyContext
    observability: ACPObservability

    @field_validator("integrity_hash")
    @classmethod
    def validate_hash(cls, value: str) -> str:
        if len(value) != 64:
            raise ValueError("integrity_hash must be a sha256 hex digest")
        return value

    def is_expired(self, now: datetime | None = None) -> bool:
        compare = now or datetime.now(tz=timezone.utc)
        age_seconds = (compare - self.timestamp_utc).total_seconds()
        return age_seconds > self.ttl_seconds


def compute_integrity_hash(payload: ACPPayload) -> str:
    canonical = dumps(payload.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    digest = sha256(canonical.encode("utf-8")).hexdigest()
    return digest
