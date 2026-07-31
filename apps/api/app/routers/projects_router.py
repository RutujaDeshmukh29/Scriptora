from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.routers.dependencies import get_current_user
from app.schemas.project_schema import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter()

def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(ProjectRepository(db))

CurrentUser = Annotated[User, Depends(get_current_user)]
ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]

@router.get("/", response_model=list[ProjectResponse])
def list_projects(current_user: CurrentUser, service: ProjectServiceDep):
    """List all active projects the user has access to."""
    projects = service.list_projects(current_user)
    return [ProjectResponse.model_validate(p) for p in projects]

@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(data: ProjectCreate, current_user: CurrentUser, service: ProjectServiceDep):
    """Create a new project."""
    project = service.create_project(data, current_user)
    return ProjectResponse.model_validate(project)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: UUID, current_user: CurrentUser, service: ProjectServiceDep):
    """Get a specific project by ID."""
    project = service.get_project(project_id, current_user)
    return ProjectResponse.model_validate(project)

@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: UUID, data: ProjectUpdate, current_user: CurrentUser, service: ProjectServiceDep):
    """Update a project."""
    project = service.update_project(project_id, data, current_user)
    return ProjectResponse.model_validate(project)

@router.delete("/{project_id}/archive", response_model=ProjectResponse)
def archive_project(project_id: UUID, current_user: CurrentUser, service: ProjectServiceDep):
    """Archive a project (owners only)."""
    project = service.archive_project(project_id, current_user)
    return ProjectResponse.model_validate(project)
