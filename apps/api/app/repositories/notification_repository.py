import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification, NotificationType


def create(db: Session, *, user_id: uuid.UUID, type: NotificationType, payload: dict[str, Any]) -> Notification:
    notification = Notification(user_id=user_id, type=type, payload=payload)
    db.add(notification)
    db.flush()
    return notification


def get_by_id(db: Session, notification_id: uuid.UUID) -> Notification | None:
    return db.get(Notification, notification_id)


def list_for_user(db: Session, user_id: uuid.UUID, *, unread_only: bool = False) -> list[Notification]:
    stmt = select(Notification).where(Notification.user_id == user_id)
    if unread_only:
        stmt = stmt.where(Notification.read.is_(False))
    stmt = stmt.order_by(Notification.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def mark_read(db: Session, notification: Notification) -> Notification:
    notification.read = True
    db.flush()
    return notification


def mark_all_read(db: Session, user_id: uuid.UUID) -> None:
    stmt = select(Notification).where(Notification.user_id == user_id, Notification.read.is_(False))
    for notification in db.execute(stmt).scalars().all():
        notification.read = True
    db.flush()
