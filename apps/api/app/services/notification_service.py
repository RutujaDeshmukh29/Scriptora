import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationType
from app.repositories import notification_repository


def notify(db: Session, *, user_id: uuid.UUID, type: NotificationType, payload: dict[str, Any]) -> Notification:
    """
    Called from WITHIN another service's transaction (e.g. project_service's
    invite_member) — deliberately flushes but does not commit, so the
    notification lands atomically with the action that triggered it. If the
    surrounding action fails and rolls back, the notification never persists
    either — which is the correct behavior.
    """
    return notification_repository.create(db, user_id=user_id, type=type, payload=payload)


def list_notifications(db: Session, user_id: uuid.UUID, *, unread_only: bool = False) -> list[Notification]:
    return notification_repository.list_for_user(db, user_id, unread_only=unread_only)


def mark_read(db: Session, notification: Notification) -> Notification:
    updated = notification_repository.mark_read(db, notification)
    db.commit()
    db.refresh(updated)
    return updated


def mark_all_read(db: Session, user_id: uuid.UUID) -> None:
    notification_repository.mark_all_read(db, user_id)
    db.commit()
