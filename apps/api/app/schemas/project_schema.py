import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.project import ProjectStatus
from app.models.project_member import ProjectRole
from app.schemas.user_schema import UserPublic


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)


class ProjectPublic(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    status: ProjectStatus
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime
    my_role: ProjectRole  # the requesting user's role on this project — not a DB column


class ProjectMemberPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    role: ProjectRole
    joined_at: datetime
    user: UserPublic


class InviteMemberRequest(BaseModel):
    email: EmailStr
    role: ProjectRole = ProjectRole.VIEWER


class UpdateMemberRoleRequest(BaseModel):
    role: ProjectRole
