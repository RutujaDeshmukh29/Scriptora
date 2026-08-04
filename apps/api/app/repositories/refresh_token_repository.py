import hashlib
import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


def hash_token(raw_token: str) -> str:
    # Refresh tokens are high-entropy random-looking strings, not user-chosen
    # secrets, so a fast hash is appropriate here (unlike passwords) — we only
    # need collision resistance for lookup, not brute-force resistance.
    return hashlib.sha256(raw_token.encode()).hexdigest()


def create(db: Session, *, user_id: uuid.UUID, raw_token: str, expires_at: datetime) -> RefreshToken:
    token = RefreshToken(user_id=user_id, token_hash=hash_token(raw_token), expires_at=expires_at)
    db.add(token)
    db.flush()
    return token


def get_by_raw_token(db: Session, raw_token: str) -> RefreshToken | None:
    token_hash = hash_token(raw_token)
    return db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash)).scalar_one_or_none()


def revoke(db: Session, token: RefreshToken) -> None:
    token.revoked = True
    db.flush()
