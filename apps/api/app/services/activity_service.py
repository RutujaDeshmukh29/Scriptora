import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.repositories import activity_repository


def log(
    db: Session,
    *,
    project_id: uuid.UUID,
    actor_id: uuid.UUID,
    action_type: str,
    target_type: str | None = None,
    target_id: uuid.UUID | None = None,
    extra_data: dict[str, Any] | None = None,
) -> ActivityLog:
    """
    Called from WITHIN another service's transaction — flushes but does not
    commit, for the same reason as notification_service.notify: the log entry
    should be part of the same atomic action, not a separate one.

    Deliberately NOT called from script autosave (script_service.update_script)
    — autosave fires on every debounced keystroke pause, and logging each one
    would flood the activity feed. Only script *creation* is logged for now.
    """
    return activity_repository.create(
        db,
        project_id=project_id,
        actor_id=actor_id,
        action_type=action_type,
        target_type=target_type,
        target_id=target_id,
        extra_data=extra_data,
    )


def list_activity(db: Session, project_id: uuid.UUID) -> list[ActivityLog]:
    return activity_repository.list_for_project(db, project_id)
