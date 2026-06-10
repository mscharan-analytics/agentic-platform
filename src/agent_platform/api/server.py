"""FastAPI server for the Enterprise Agent Platform."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from agent_platform.api.routes import agents, auth, events, health, mcp_tools, models, ollama

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[no-untyped-def]
    """Manage FastAPI lifespan (startup/shutdown)."""
    logger.info("Starting Enterprise Agent Platform API")
    yield
    logger.info("Shutting down Enterprise Agent Platform API")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Enterprise Agent Platform API",
        description="REST API for agent orchestration, MCP tools, and model management",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS configuration for web UI
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Dev UIs
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> JSONResponse:
        """Platform health check."""
        return JSONResponse({"status": "ok", "service": "agent-platform"})

    # Include routers
    app.include_router(health.router, prefix="/api/health", tags=["health"])
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
    app.include_router(mcp_tools.router, prefix="/api/tools", tags=["tools"])
    app.include_router(models.router, prefix="/api/models", tags=["models"])
    app.include_router(ollama.router, prefix="/api/ollama", tags=["ollama"])
    app.include_router(events.router, prefix="/api/events", tags=["events"])

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

