import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.script import Script


def create_script(
    db: Session, *, project_id: uuid.UUID, title: str, parent_folder_id: uuid.UUID | None, created_by: uuid.UUID
) -> Script:
    script = Script(project_id=project_id, title=title, parent_folder_id=parent_folder_id, created_by=created_by)
    db.add(script)
    db.flush()
    return script


def get_by_id(db: Session, script_id: uuid.UUID) -> Script | None:
    return db.get(Script, script_id)


def list_for_project(db: Session, project_id: uuid.UUID) -> list[Script]:
    stmt = select(Script).where(Script.project_id == project_id).order_by(Script.updated_at.desc())
    return list(db.execute(stmt).scalars().all())


def delete(db: Session, script: Script) -> None:
    db.delete(script)
    db.flush()
