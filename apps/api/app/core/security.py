"""
Password hashing and JWT creation/verification.

Import create_access_token, create_refresh_token, and decode_token from here
wherever auth is needed — never build or parse a JWT by hand elsewhere, so
there is exactly one place that knows the token format.
"""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# --- Password hashing ---

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


# --- JWT creation ---

TokenType = Literal["access", "refresh"]


def _create_token(subject: str, expires_delta: timedelta, token_type: TokenType) -> str:
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    payload = {
        "sub": subject,             # who the token belongs to — the user's id
        "type": token_type,          # "access" or "refresh" — routes check this
        "iat": int(now.timestamp()),   # issued-at, standard JWT claim (NumericDate)
        "exp": int(expire.timestamp()),  # expiry, standard JWT claim
        "jti": str(uuid.uuid4()),          # unique token id, for future revocation
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: uuid.UUID) -> str:
    return _create_token(
        subject=str(user_id),
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MINUTES),
        token_type="access",
    )


def create_refresh_token(user_id: uuid.UUID) -> str:
    return _create_token(
        subject=str(user_id),
        expires_delta=timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS),
        token_type="refresh",
    )


# --- JWT verification ---

class TokenError(Exception):
    """Raised for any invalid, expired, or wrong-type token."""


def decode_token(token: str, expected_type: TokenType | None = None) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise TokenError("Invalid or expired token") from exc

    if expected_type is not None and payload.get("type") != expected_type:
        raise TokenError(f"Expected a '{expected_type}' token, got '{payload.get('type')}'")

    return payload
