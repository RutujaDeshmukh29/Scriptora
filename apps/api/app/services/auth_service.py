from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    TokenError,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories import refresh_token_repository, user_repository


class EmailAlreadyExistsError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class InvalidRefreshTokenError(Exception):
    pass


def register_user(db: Session, *, name: str, email: str, password: str) -> User:
    if user_repository.get_by_email(db, email) is not None:
        raise EmailAlreadyExistsError(email)

    user = user_repository.create(db, name=name, email=email, password_hash=hash_password(password))
    db.commit()
    db.refresh(user)
    return user

def update_user_profile(db: Session, user: User, update_data: dict) -> User:
    updated_user = user_repository.update(db, user=user, update_data=update_data)
    db.commit()
    db.refresh(updated_user)
    return updated_user


def authenticate_user(db: Session, *, email: str, password: str) -> User:
    user = user_repository.get_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        # Deliberately the same error for "no such user" and "wrong password" —
        # distinguishing them lets an attacker enumerate valid emails.
        raise InvalidCredentialsError()
    return user


def issue_tokens(db: Session, user: User) -> tuple[str, str]:
    """Creates a fresh access + refresh token pair and persists the refresh token's hash."""
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS)
    refresh_token_repository.create(db, user_id=user.id, raw_token=refresh_token, expires_at=expires_at)
    db.commit()

    return access_token, refresh_token


def rotate_refresh_token(db: Session, raw_refresh_token: str) -> tuple[User, str, str]:
    """
    Validates a refresh token, revokes it, and issues a brand new access +
    refresh token pair. Refresh tokens are single-use: reusing an old one
    (e.g. a stolen, already-rotated token) always fails.
    """
    try:
        payload = decode_token(raw_refresh_token, expected_type="refresh")
    except TokenError as exc:
        raise InvalidRefreshTokenError() from exc

    stored = refresh_token_repository.get_by_raw_token(db, raw_refresh_token)
    if stored is None or stored.revoked or stored.expires_at < datetime.now(timezone.utc):
        raise InvalidRefreshTokenError()

    user = user_repository.get_by_id(db, stored.user_id)
    if user is None or str(user.id) != payload["sub"]:
        raise InvalidRefreshTokenError()

    refresh_token_repository.revoke(db, stored)
    new_access_token, new_refresh_token = issue_tokens(db, user)
    return user, new_access_token, new_refresh_token


def revoke_refresh_token(db: Session, raw_refresh_token: str) -> None:
    stored = refresh_token_repository.get_by_raw_token(db, raw_refresh_token)
    if stored is not None and not stored.revoked:
        refresh_token_repository.revoke(db, stored)
        db.commit()
