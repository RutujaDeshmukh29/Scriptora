"""
Import every model here so that:
  1. `Base.metadata` knows about all tables (required for Alembic autogenerate).
  2. String-based relationship references (e.g. "ProjectMember") resolve correctly
     no matter which module is imported first.

Add every new model's import to this file the moment it's created.
"""
from app.models.organization import Organization
from app.models.project import Project, ProjectStatus
from app.models.project_member import ProjectMember, ProjectRole
from app.models.script import Script
from app.models.user import User

__all__ = [
    "User",
    "Organization",
    "Project",
    "ProjectStatus",
    "ProjectMember",
    "ProjectRole",
    "Script",
]
