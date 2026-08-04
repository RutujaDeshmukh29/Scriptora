import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.project import Project
from app.models.project_member import ProjectMember, ProjectRole


def create_project(
    db: Session, *, name: str, description: str | None, organization_id: uuid.UUID | None, created_by: uuid.UUID
) -> Project:
    project = Project(name=name, description=description, organization_id=organization_id, created_by=created_by)
    db.add(project)
    db.flush()
    return project


def get_by_id(db: Session, project_id: uuid.UUID) -> Project | None:
    return db.get(Project, project_id)


def list_for_user(db: Session, user_id: uuid.UUID) -> list[ProjectMember]:
    """Returns this user's ProjectMember rows, each with .project eagerly loaded."""
    stmt = select(ProjectMember).where(ProjectMember.user_id == user_id).options(joinedload(ProjectMember.project))
    return list(db.execute(stmt).scalars().all())


def get_membership(db: Session, *, project_id: uuid.UUID, user_id: uuid.UUID) -> ProjectMember | None:
    stmt = select(ProjectMember).where(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def list_members(db: Session, project_id: uuid.UUID) -> list[ProjectMember]:
    stmt = (
        select(ProjectMember)
        .where(ProjectMember.project_id == project_id)
        .options(joinedload(ProjectMember.user))
    )
    return list(db.execute(stmt).scalars().all())


def add_member(db: Session, *, project_id: uuid.UUID, user_id: uuid.UUID, role: ProjectRole) -> ProjectMember:
    member = ProjectMember(project_id=project_id, user_id=user_id, role=role)
    db.add(member)
    db.flush()
    return member


def remove_member(db: Session, membership: ProjectMember) -> None:
    db.delete(membership)
    db.flush()


def update_member_role(db: Session, membership: ProjectMember, role: ProjectRole) -> ProjectMember:
    membership.role = role
    db.flush()
    return membership
