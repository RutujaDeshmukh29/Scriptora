from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.project import Project, ProjectStatus
from app.models.project_member import ProjectMember, ProjectRole


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, project_id: UUID) -> Project | None:
        return self.session.query(Project).filter(Project.id == project_id).first()

    def list_by_user(self, user_id: UUID) -> list[Project]:
        # Get projects where the user is a member
        return (
            self.session.query(Project)
            .join(ProjectMember, ProjectMember.project_id == Project.id)
            .filter(ProjectMember.user_id == user_id)
            .filter(Project.status == ProjectStatus.ACTIVE)
            .all()
        )

    def create(self, project_data: dict[str, Any], user_id: UUID) -> Project:
        project = Project(**project_data, created_by=user_id)
        self.session.add(project)
        self.session.flush() # flush to get project.id
        
        # Add creator as owner
        member = ProjectMember(project_id=project.id, user_id=user_id, role=ProjectRole.OWNER)
        self.session.add(member)
        self.session.commit()
        self.session.refresh(project)
        return project

    def update(self, project: Project, update_data: dict[str, Any]) -> Project:
        for field, value in update_data.items():
            setattr(project, field, value)
        self.session.commit()
        self.session.refresh(project)
        return project

    def get_member(self, project_id: UUID, user_id: UUID) -> ProjectMember | None:
        return (
            self.session.query(ProjectMember)
            .filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
            .first()
        )
