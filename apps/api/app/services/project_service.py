import uuid

from sqlalchemy.orm import Session

from app.models.notification import NotificationType
from app.models.project import Project, ProjectStatus
from app.models.project_member import ProjectMember, ProjectRole
from app.models.user import User
from app.repositories import project_repository, user_repository
from app.services import activity_service, notification_service


class UserNotFoundError(Exception):
    """Raised when inviting by an email with no registered account (no email-invite flow yet)."""


class AlreadyAMemberError(Exception):
    pass


class CannotRemoveLastOwnerError(Exception):
    pass


def create_project(db: Session, *, name: str, description: str | None, owner: User) -> Project:
    project = project_repository.create_project(
        db, name=name, description=description, organization_id=None, created_by=owner.id
    )
    project_repository.add_member(db, project_id=project.id, user_id=owner.id, role=ProjectRole.OWNER)
    activity_service.log(db, project_id=project.id, actor_id=owner.id, action_type="project_created")
    db.commit()
    db.refresh(project)
    return project


def list_projects_for_user(db: Session, user_id: uuid.UUID) -> list[tuple[Project, ProjectRole]]:
    memberships = project_repository.list_for_user(db, user_id)
    return [(m.project, m.role) for m in memberships]


def update_project(db: Session, project: Project, *, name: str | None, description: str | None) -> Project:
    if name is not None:
        project.name = name
    if description is not None:
        project.description = description
    db.commit()
    db.refresh(project)
    return project


def archive_project(db: Session, project: Project) -> Project:
    project.status = ProjectStatus.ARCHIVED
    db.commit()
    db.refresh(project)
    return project


def invite_member(
    db: Session, *, project_id: uuid.UUID, email: str, role: ProjectRole, invited_by: uuid.UUID
) -> ProjectMember:
    user = user_repository.get_by_email(db, email)
    if user is None:
        raise UserNotFoundError(email)

    if project_repository.get_membership(db, project_id=project_id, user_id=user.id) is not None:
        raise AlreadyAMemberError()

    member = project_repository.add_member(db, project_id=project_id, user_id=user.id, role=role)

    project = project_repository.get_by_id(db, project_id)
    project_name = project.name if project else "a project"

    activity_service.log(
        db,
        project_id=project_id,
        actor_id=invited_by,
        action_type="member_joined",
        target_type="user",
        target_id=user.id,
        extra_data={"role": role.value},
    )
    notification_service.notify(
        db,
        user_id=user.id,
        type=NotificationType.PROJECT_INVITE,
        payload={"project_id": str(project_id), "project_name": project_name, "role": role.value},
    )

    db.commit()
    db.refresh(member)
    return member


def _has_another_owner(db: Session, *, project_id: uuid.UUID, excluding_user_id: uuid.UUID) -> bool:
    return any(
        m.role == ProjectRole.OWNER and m.user_id != excluding_user_id
        for m in project_repository.list_members(db, project_id)
    )


def remove_member(
    db: Session, *, project_id: uuid.UUID, membership_to_remove: ProjectMember, actor_id: uuid.UUID
) -> None:
    if membership_to_remove.role == ProjectRole.OWNER and not _has_another_owner(
        db, project_id=project_id, excluding_user_id=membership_to_remove.user_id
    ):
        raise CannotRemoveLastOwnerError()

    removed_user_id = membership_to_remove.user_id
    project_repository.remove_member(db, membership_to_remove)

    activity_service.log(
        db,
        project_id=project_id,
        actor_id=actor_id,
        action_type="member_removed",
        target_type="user",
        target_id=removed_user_id,
    )

    db.commit()


def update_member_role(
    db: Session, *, project_id: uuid.UUID, membership: ProjectMember, new_role: ProjectRole, actor_id: uuid.UUID
) -> ProjectMember:
    if (
        membership.role == ProjectRole.OWNER
        and new_role != ProjectRole.OWNER
        and not _has_another_owner(db, project_id=project_id, excluding_user_id=membership.user_id)
    ):
        raise CannotRemoveLastOwnerError()

    old_role = membership.role
    updated = project_repository.update_member_role(db, membership, new_role)

    activity_service.log(
        db,
        project_id=project_id,
        actor_id=actor_id,
        action_type="member_role_changed",
        target_type="user",
        target_id=membership.user_id,
        extra_data={"old_role": old_role.value, "new_role": new_role.value},
    )

    db.commit()
    db.refresh(updated)
    return updated
