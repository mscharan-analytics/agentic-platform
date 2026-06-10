"""Health check endpoints."""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def get_status() -> dict[str, object]:
    """Get platform health status."""
    return {
        "service": "agent-platform",
        "status": "healthy",
        "version": "0.1.0",
    }


@router.get("/ready")
async def get_ready() -> dict[str, object]:
    """Readiness probe for Kubernetes."""
    return {"ready": True}
