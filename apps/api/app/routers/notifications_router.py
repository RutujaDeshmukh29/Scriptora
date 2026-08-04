import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.repositories import notification_repository
from app.schemas.notification_schema import NotificationPublic
from app.services import notification_service

router = APIRouter()


@router.get("/notifications", response_model=list[NotificationPublic])
def list_notifications(
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[NotificationPublic]:
    notifications = notification_service.list_notifications(db, current_user.id, unread_only=unread_only)
    return [NotificationPublic.model_validate(n) for n in notifications]


@router.patch("/notifications/{notification_id}/read", response_model=NotificationPublic)
def mark_read(
    notification_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NotificationPublic:
    notification = notification_repository.get_by_id(db, notification_id)
    if notification is None or notification.user_id != current_user.id:
        # 404 either way — don't reveal whether a notification ID belongs to someone else.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    updated = notification_service.mark_read(db, notification)
    return NotificationPublic.model_validate(updated)


@router.post("/notifications/read-all", status_code=status.HTTP_204_NO_CONTENT)
def mark_all_read(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    notification_service.mark_all_read(db, current_user.id)
