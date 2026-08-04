from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.comment import Comment
from app.models.project_member import ProjectMember, ProjectRole
from app.models.script import Script
from app.models.user import User
from app.schemas.comment_schema import CommentCreate, CommentPublic, CommentReplyCreate, CommentReplyPublic
from app.services import comment_service
from app.utils.permissions import require_comment_role, require_script_access, require_script_role
from app.middleware.auth_middleware import get_current_user

router = APIRouter()


@router.get("/scripts/{script_id}/comments", response_model=list[CommentPublic])
def list_comments(
    access: tuple[Script, ProjectMember] = Depends(require_script_access),
    db: Session = Depends(get_db),
) -> list[CommentPublic]:
    script, _ = access
    comments = comment_service.list_comments(db, script.id)
    return [CommentPublic.model_validate(c) for c in comments]


@router.post("/scripts/{script_id}/comments", response_model=CommentPublic, status_code=status.HTTP_201_CREATED)
def create_comment(
    payload: CommentCreate,
    access: tuple[Script, ProjectMember] = Depends(require_script_role(ProjectRole.OWNER, ProjectRole.EDITOR)),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CommentPublic:
    script, _ = access
    comment = comment_service.create_comment(
        db,
        script=script,
        author_id=current_user.id,
        content=payload.content,
        anchor_from=payload.anchor_from,
        anchor_to=payload.anchor_to,
        quoted_text=payload.quoted_text,
    )
    return CommentPublic.model_validate(comment)


@router.post("/comments/{comment_id}/replies", response_model=CommentReplyPublic, status_code=status.HTTP_201_CREATED)
def add_reply(
    payload: CommentReplyCreate,
    comment: Comment = Depends(require_comment_role(ProjectRole.OWNER, ProjectRole.EDITOR)),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CommentReplyPublic:
    reply = comment_service.add_reply(db, comment_id=comment.id, author_id=current_user.id, content=payload.content)
    return CommentReplyPublic.model_validate(reply)


@router.patch("/comments/{comment_id}/resolve", response_model=CommentPublic)
def resolve_comment(
    comment: Comment = Depends(require_comment_role(ProjectRole.OWNER, ProjectRole.EDITOR)),
    db: Session = Depends(get_db),
) -> CommentPublic:
    updated = comment_service.set_resolved(db, comment, True)
    return CommentPublic.model_validate(updated)


@router.patch("/comments/{comment_id}/reopen", response_model=CommentPublic)
def reopen_comment(
    comment: Comment = Depends(require_comment_role(ProjectRole.OWNER, ProjectRole.EDITOR)),
    db: Session = Depends(get_db),
) -> CommentPublic:
    updated = comment_service.set_resolved(db, comment, False)
    return CommentPublic.model_validate(updated)
