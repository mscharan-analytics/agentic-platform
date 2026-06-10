from datetime import datetime, timezone

from agent_platform.contracts.a2a import A2AEnvelope, A2AMessageType, AuthContext
from agent_platform.contracts.acp import (
    ACPEnvelope,
    ACPObservability,
    ACPPayload,
    ACPPolicyContext,
    ACPProvenance,
    compute_integrity_hash,
)


def test_acp_integrity_hash_has_sha256_length() -> None:
    payload = ACPPayload(objective_summary="Ship release")
    digest = compute_integrity_hash(payload)
    assert len(digest) == 64


def test_a2a_envelope_creation() -> None:
    envelope = A2AEnvelope(
        message_type=A2AMessageType.REQUEST,
        sender_agent_id="solver-agent",
        receiver_agent_id="planner-agent",
        auth_context=AuthContext(actor_role="solver", auth_token_ref="token-1"),
        policy_decision_ref="decision-1",
    )
    assert envelope.message_type == A2AMessageType.REQUEST
    assert envelope.sender_agent_id == "solver-agent"


def test_acp_envelope_creation() -> None:
    payload = ACPPayload(objective_summary="Build autonomous flow")
    envelope = ACPEnvelope(
        sender_agent_id="orchestrator-agent",
        recipient_agent_id="worker-code-agent",
        integrity_hash=compute_integrity_hash(payload),
        provenance=ACPProvenance(
            source_refs=["goal"],
            collected_by_agent="orchestrator-agent",
            collected_at_utc=datetime.now(timezone.utc),
            confidence_score=0.95,
        ),
        context_payload=payload,
        policy_context=ACPPolicyContext(),
        observability=ACPObservability(span_id="span-1"),
    )
    assert envelope.protocol_name == "ACP"
    assert not envelope.is_expired()
