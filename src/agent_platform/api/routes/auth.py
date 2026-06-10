"""Authentication routes (login, token refresh)."""

from __future__ import annotations

import logging
from pydantic import BaseModel

from fastapi import APIRouter, HTTPException

from agent_platform.api.auth import create_access_token, TokenResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Simple in-memory user store (replace with database in production)
DEMO_USERS = {
    "admin": "admin",  # username: password (DO NOT USE IN PRODUCTION)
    "user": "password",
}


class LoginRequest(BaseModel):
    """Login request body."""
    username: str
    password: str


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    """Authenticate and return access token."""
    username = request.username
    password = request.password
    
    if username not in DEMO_USERS or DEMO_USERS[username] != password:
        logger.warning(f"Failed login attempt for user: {username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Determine role
    role = "admin" if username == "admin" else "user"

    # Create token
    token = create_access_token(subject=username, role=role)

    logger.info(f"User {username} logged in")

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=3600,
    )


@router.post("/token", response_model=TokenResponse)
async def get_token(username: str, password: str) -> TokenResponse:
    """Alias for /login for compatibility."""
    return await login(username, password)


@router.get("/me")
async def get_current_user(token: str | None = None) -> dict[str, object]:
    """Get current user info (requires valid token)."""
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        from agent_platform.api.auth import verify_token

        token_data = verify_token(token)
        return {
            "username": token_data.sub,
            "role": token_data.role,
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
