from uuid import UUID

from fastapi import HTTPException, status

from app.models.project import Project, ProjectStatus
from app.models.project_member import ProjectRole
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.schemas.project_schema import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, project_repo: ProjectRepository):
        self.project_repo = project_repo

    def list_projects(self, user: User) -> list[Project]:
        return self.project_repo.list_by_user(user.id)

    def create_project(self, data: ProjectCreate, user: User) -> Project:
        return self.project_repo.create(data.model_dump(), user.id)

    def get_project(self, project_id: UUID, user: User) -> Project:
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        member = self.project_repo.get_member(project_id, user.id)
        if not member:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        return project

    def update_project(self, project_id: UUID, data: ProjectUpdate, user: User) -> Project:
        project = self.get_project(project_id, user)
        member = self.project_repo.get_member(project_id, user.id)
        
        # Only OWNER or EDITOR can update project details
        if member.role not in (ProjectRole.OWNER, ProjectRole.EDITOR):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

        update_data = data.model_dump(exclude_unset=True)
        return self.project_repo.update(project, update_data)

    def archive_project(self, project_id: UUID, user: User) -> Project:
        project = self.get_project(project_id, user)
        member = self.project_repo.get_member(project_id, user.id)
        
        # Only OWNER can archive a project
        if member.role != ProjectRole.OWNER:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owners can archive projects")

        return self.project_repo.update(project, {"status": ProjectStatus.ARCHIVED})
