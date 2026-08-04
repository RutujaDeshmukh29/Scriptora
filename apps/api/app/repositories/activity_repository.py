import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.activity_log import ActivityLog


def create(
    db: Session,
    *,
    project_id: uuid.UUID,
    actor_id: uuid.UUID,
    action_type: str,
    target_type: str | None = None,
    target_id: uuid.UUID | None = None,
    extra_data: dict[str, Any] | None = None,
) -> ActivityLog:
    entry = ActivityLog(
        project_id=project_id,
        actor_id=actor_id,
        action_type=action_type,
        target_type=target_type,
        target_id=target_id,
        extra_data=extra_data or {},
    )
    db.add(entry)
    db.flush()
    return entry


def list_for_project(db: Session, project_id: uuid.UUID, *, limit: int = 50) -> list[ActivityLog]:
    stmt = (
        select(ActivityLog)
        .where(ActivityLog.project_id == project_id)
        .options(joinedload(ActivityLog.actor))
        .order_by(ActivityLog.created_at.desc())
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())
