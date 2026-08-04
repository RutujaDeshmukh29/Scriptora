import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project_member import ProjectMember, ProjectRole
from app.models.script import Script
from app.schemas.script_schema import ScriptCreate, ScriptPublic, ScriptSummary, ScriptUpdate
from app.services import script_service
from app.utils.permissions import require_project_access, require_role, require_script_access, require_script_role

router = APIRouter()


@router.post("/projects/{project_id}/scripts", response_model=ScriptPublic, status_code=status.HTTP_201_CREATED)
def create_script(
    project_id: uuid.UUID,
    payload: ScriptCreate,
    membership: ProjectMember = Depends(require_role(ProjectRole.OWNER, ProjectRole.EDITOR)),
    db: Session = Depends(get_db),
) -> ScriptPublic:
    script = script_service.create_script(
        db,
        project_id=project_id,
        title=payload.title,
        parent_folder_id=payload.parent_folder_id,
        created_by=membership.user_id,
    )
    return ScriptPublic.model_validate(script)


@router.get("/projects/{project_id}/scripts", response_model=list[ScriptSummary])
def list_scripts(
    project_id: uuid.UUID,
    membership: ProjectMember = Depends(require_project_access),
    db: Session = Depends(get_db),
) -> list[ScriptSummary]:
    scripts = script_service.list_scripts(db, project_id)
    return [ScriptSummary.model_validate(s) for s in scripts]


@router.get("/scripts/{script_id}", response_model=ScriptPublic)
def get_script(access: tuple[Script, ProjectMember] = Depends(require_script_access)) -> ScriptPublic:
    script, _ = access
    return ScriptPublic.model_validate(script)


@router.patch("/scripts/{script_id}", response_model=ScriptPublic)
def update_script(
    payload: ScriptUpdate,
    access: tuple[Script, ProjectMember] = Depends(require_script_role(ProjectRole.OWNER, ProjectRole.EDITOR)),
    db: Session = Depends(get_db),
) -> ScriptPublic:
    script, _ = access
    updated = script_service.update_script(db, script, title=payload.title, content=payload.content)
    return ScriptPublic.model_validate(updated)


@router.delete("/scripts/{script_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_script(
    access: tuple[Script, ProjectMember] = Depends(require_script_role(ProjectRole.OWNER, ProjectRole.EDITOR)),
    db: Session = Depends(get_db),
) -> None:
    script, _ = access
    script_service.delete_script(db, script)
