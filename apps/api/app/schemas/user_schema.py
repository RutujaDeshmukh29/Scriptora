import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    email: EmailStr
    avatar_url: str | None
    theme: str

class UserUpdate(BaseModel):
    name: str | None = None
    avatar_url: str | None = None
