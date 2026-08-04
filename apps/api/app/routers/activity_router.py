from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project_member import ProjectMember
from app.schemas.activity_schema import ActivityLogPublic
from app.services import activity_service
from app.utils.permissions import require_project_access

router = APIRouter()


@router.get("/projects/{project_id}/activity", response_model=list[ActivityLogPublic])
def list_activity(
    membership: ProjectMember = Depends(require_project_access),
    db: Session = Depends(get_db),
) -> list[ActivityLogPublic]:
    entries = activity_service.list_activity(db, membership.project_id)
    return [ActivityLogPublic.model_validate(e) for e in entries]
