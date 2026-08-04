import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.schemas.user_schema import UserPublic


class ActivityLogPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    action_type: str
    target_type: str | None
    target_id: uuid.UUID | None
    extra_data: dict[str, Any]
    actor: UserPublic
    created_at: datetime
