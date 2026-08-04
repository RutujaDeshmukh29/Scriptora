import uuid

from sqlalchemy.orm import Session

from app.models.script import Script
from app.repositories import script_repository
from app.services import activity_service


def create_script(
    db: Session, *, project_id: uuid.UUID, title: str | None, parent_folder_id: uuid.UUID | None, created_by: uuid.UUID
) -> Script:
    script = script_repository.create_script(
        db,
        project_id=project_id,
        title=title or "Untitled Script",
        parent_folder_id=parent_folder_id,
        created_by=created_by,
    )
    activity_service.log(
        db,
        project_id=project_id,
        actor_id=created_by,
        action_type="script_created",
        target_type="script",
        target_id=script.id,
        extra_data={"title": script.title},
    )
    db.commit()
    db.refresh(script)
    return script


def list_scripts(db: Session, project_id: uuid.UUID) -> list[Script]:
    return script_repository.list_for_project(db, project_id)


def update_script(db: Session, script: Script, *, title: str | None, content: str | None) -> Script:
    # No activity_service.log() call here on purpose — this fires on every
    # debounced autosave (roughly once per second of active typing), and
    # logging each one would flood the project's activity feed. Only
    # script *creation* is logged; edits are implicit in updated_at.
    if title is not None:
        script.title = title
    if content is not None:
        script.content = content
    db.commit()
    db.refresh(script)
    return script


def delete_script(db: Session, script: Script) -> None:
    script_repository.delete(db, script)
    db.commit()
