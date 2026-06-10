"""JWT authentication utilities."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import jwt
from pydantic import BaseModel

# Use env var or fallback for development
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class TokenData(BaseModel):
    """JWT token payload."""

    sub: str  # subject (username)
    role: str = "user"  # role (admin, user, etc.)
    exp: datetime | None = None


class TokenResponse(BaseModel):
    """Token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


def create_access_token(
    subject: str,
    role: str = "user",
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": subject,
        "role": role,
        "exp": expire,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject: str = payload.get("sub")
        role: str = payload.get("role", "user")

        if subject is None:
            raise ValueError("Invalid token: no subject")

        return TokenData(sub=subject, role=role)
    except jwt.ExpiredSignatureError as e:
        raise ValueError("Token has expired") from e
    except jwt.InvalidTokenError as e:
        raise ValueError("Invalid token") from e


def get_token_from_header(auth_header: str | None) -> str:
    """Extract token from Authorization header."""
    if not auth_header:
        raise ValueError("Missing authorization header")

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ValueError("Invalid authorization header format")

    return parts[1]
