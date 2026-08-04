import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user_schema import UserPublic


class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
    anchor_from: int | None = None
    anchor_to: int | None = None
    quoted_text: str | None = Field(default=None, max_length=500)


class CommentReplyCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)


class CommentReplyPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    content: str
    author: UserPublic
    created_at: datetime


class CommentPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    script_id: uuid.UUID
    content: str
    anchor_from: int | None
    anchor_to: int | None
    quoted_text: str | None
    resolved: bool
    author: UserPublic
    replies: list[CommentReplyPublic]
    created_at: datetime
