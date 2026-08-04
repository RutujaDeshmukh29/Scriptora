import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ScriptCreate(BaseModel):
    title: str = Field(default="Untitled Script", max_length=200)
    parent_folder_id: uuid.UUID | None = None


class ScriptUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    content: str | None = None


class ScriptSummary(BaseModel):
    """Used for list views — deliberately excludes `content` so listing 50
    scripts doesn't ship 50 full documents over the wire."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    updated_at: datetime


class ScriptPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    parent_folder_id: uuid.UUID | None
    title: str
    content: str | None
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime
