import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.project import Project
from app.models.project_member import ProjectMember, ProjectRole
from app.models.user import User
from app.repositories import project_repository
from app.schemas.project_schema import (
    InviteMemberRequest,
    ProjectCreate,
    ProjectMemberPublic,
    ProjectPublic,
    ProjectUpdate,
    UpdateMemberRoleRequest,
)
from app.services import project_service
from app.utils.permissions import require_project_access, require_role

router = APIRouter()


def _to_project_public(project: Project, my_role: ProjectRole) -> ProjectPublic:
    return ProjectPublic(
        id=project.id,
        name=project.name,
        description=project.description,
        status=project.status,
        created_by=project.created_by,
        created_at=project.created_at,
        updated_at=project.updated_at,
        my_role=my_role,
    )


@router.post("", response_model=ProjectPublic, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> ProjectPublic:
    project = project_service.create_project(db, name=payload.name, description=payload.description, owner=current_user)
    return _to_project_public(project, ProjectRole.OWNER)


@router.get("", response_model=list[ProjectPublic])
def list_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[ProjectPublic]:
    results = project_service.list_projects_for_user(db, current_user.id)
    return [_to_project_public(project, role) for project, role in results]


@router.get("/{project_id}", response_model=ProjectPublic)
def get_project(project_id: uuid.UUID, membership: ProjectMember = Depends(require_project_access)) -> ProjectPublic:
    return _to_project_public(membership.project, membership.role)


@router.patch("/{project_id}", response_model=ProjectPublic)
def update_project(
    project_id: uuid.UUID,
    payload: ProjectUpdate,
    membership: ProjectMember = Depends(require_role(ProjectRole.OWNER)),
    db: Session = Depends(get_db),
) -> ProjectPublic:
    project = project_service.update_project(db, membership.project, name=payload.name, description=payload.description)
    return _to_project_public(project, membership.role)


@router.post("/{project_id}/archive", response_model=ProjectPublic)
def archive_project(
    project_id: uuid.UUID,
    membership: ProjectMember = Depends(require_role(ProjectRole.OWNER)),
    db: Session = Depends(get_db),
) -> ProjectPublic:
    project = project_service.archive_project(db, membership.project)
    return _to_project_public(project, membership.role)


@router.get("/{project_id}/members", response_model=list[ProjectMemberPublic])
def list_members(
    project_id: uuid.UUID,
    membership: ProjectMember = Depends(require_project_access),
    db: Session = Depends(get_db),
) -> list[ProjectMemberPublic]:
    members = project_repository.list_members(db, project_id)
    return [ProjectMemberPublic.model_validate(m) for m in members]


@router.post("/{project_id}/members", response_model=ProjectMemberPublic, status_code=status.HTTP_201_CREATED)
def invite_member(
    project_id: uuid.UUID,
    payload: InviteMemberRequest,
    membership: ProjectMember = Depends(require_role(ProjectRole.OWNER)),
    db: Session = Depends(get_db),
) -> ProjectMemberPublic:
    try:
        member = project_service.invite_member(
            db, project_id=project_id, email=payload.email, role=payload.role, invited_by=membership.user_id
        )
    except project_service.UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account exists with that email yet — they need to register first",
        ) from exc
    except project_service.AlreadyAMemberError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This user is already a member of the project"
        ) from exc
    return ProjectMemberPublic.model_validate(member)


@router.delete("/{project_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    project_id: uuid.UUID,
    user_id: uuid.UUID,
    membership: ProjectMember = Depends(require_role(ProjectRole.OWNER)),
    db: Session = Depends(get_db),
) -> None:
    target = project_repository.get_membership(db, project_id=project_id, user_id=user_id)
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    try:
        project_service.remove_member(
            db, project_id=project_id, membership_to_remove=target, actor_id=membership.user_id
        )
    except project_service.CannotRemoveLastOwnerError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Cannot remove the last owner of a project"
        ) from exc


@router.patch("/{project_id}/members/{user_id}", response_model=ProjectMemberPublic)
def update_member_role(
    project_id: uuid.UUID,
    user_id: uuid.UUID,
    payload: UpdateMemberRoleRequest,
    membership: ProjectMember = Depends(require_role(ProjectRole.OWNER)),
    db: Session = Depends(get_db),
) -> ProjectMemberPublic:
    target = project_repository.get_membership(db, project_id=project_id, user_id=user_id)
    if target is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    try:
        updated = project_service.update_member_role(
            db, project_id=project_id, membership=target, new_role=payload.role, actor_id=membership.user_id
        )
    except project_service.CannotRemoveLastOwnerError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Cannot demote the last owner of a project"
        ) from exc
    return ProjectMemberPublic.model_validate(updated)
