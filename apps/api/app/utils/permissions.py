import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.comment import Comment
from app.models.project_member import ProjectMember, ProjectRole
from app.models.script import Script
from app.models.user import User
from app.repositories import comment_repository, project_repository, script_repository


def require_project_access(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectMember:
    """
    Any project member (any role) can pass this — used on every project-scoped
    route as the base access check. Returns the caller's membership row, which
    routes can read .role from without a second query.
    """
    membership = project_repository.get_membership(db, project_id=project_id, user_id=current_user.id)
    if membership is None:
        # 404, not 403 — a non-member shouldn't be able to tell a private
        # project exists at all just by probing the URL.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return membership


def require_role(*allowed_roles: ProjectRole):
    """
    Dependency factory for stricter checks:
        membership: ProjectMember = Depends(require_role(ProjectRole.OWNER))
    Composes on top of require_project_access, so 404-before-403 still applies.
    """

    def dependency(membership: ProjectMember = Depends(require_project_access)) -> ProjectMember:
        if membership.role not in allowed_roles:
            allowed = ", ".join(role.value for role in allowed_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of these roles: {allowed}",
            )
        return membership

    return dependency


def require_script_access(
    script_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> tuple[Script, ProjectMember]:
    """
    A script has no roles of its own — access is entirely inherited from its
    parent project's membership. Returns (script, caller's membership).
    """
    script = script_repository.get_by_id(db, script_id)
    if script is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")

    membership = project_repository.get_membership(db, project_id=script.project_id, user_id=current_user.id)
    if membership is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")

    return script, membership


def require_script_role(*allowed_roles: ProjectRole):
    def dependency(access: tuple[Script, ProjectMember] = Depends(require_script_access)) -> tuple[Script, ProjectMember]:
        _, membership = access
        if membership.role not in allowed_roles:
            allowed = ", ".join(role.value for role in allowed_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of these roles: {allowed}",
            )
        return access

    return dependency


def require_comment_role(*allowed_roles: ProjectRole):
    """
    A comment has no role of its own — access is inherited through its script's
    parent project, exactly like require_script_role but one hop further down.
    """

    def dependency(
        comment_id: uuid.UUID,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> Comment:
        comment = comment_repository.get_by_id(db, comment_id)
        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

        membership = project_repository.get_membership(
            db, project_id=comment.script.project_id, user_id=current_user.id
        )
        if membership is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

        if allowed_roles and membership.role not in allowed_roles:
            allowed = ", ".join(role.value for role in allowed_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of these roles: {allowed}",
            )

        return comment

    return dependency
