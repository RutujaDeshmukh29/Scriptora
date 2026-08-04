import uuid

from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.models.comment_reply import CommentReply
from app.models.notification import NotificationType
from app.models.script import Script
from app.repositories import comment_repository
from app.services import activity_service, notification_service


def create_comment(
    db: Session,
    *,
    script: Script,
    author_id: uuid.UUID,
    content: str,
    anchor_from: int | None,
    anchor_to: int | None,
    quoted_text: str | None,
) -> Comment:
    comment = comment_repository.create_comment(
        db,
        script_id=script.id,
        author_id=author_id,
        content=content,
        anchor_from=anchor_from,
        anchor_to=anchor_to,
        quoted_text=quoted_text,
    )

    activity_service.log(
        db,
        project_id=script.project_id,
        actor_id=author_id,
        action_type="comment_added",
        target_type="script",
        target_id=script.id,
    )

    # Minimal notification scope for V1: notify the script's creator when
    # someone else comments. Fanning out to every project member (or thread
    # participants) is a reasonable next step but adds real complexity —
    # deferred, noted in ROADMAP.md's Phase 2/3.
    if script.created_by != author_id:
        notification_service.notify(
            db,
            user_id=script.created_by,
            type=NotificationType.NEW_COMMENT,
            payload={"script_id": str(script.id), "script_title": script.title, "comment_id": str(comment.id)},
        )

    db.commit()
    db.refresh(comment)
    return comment


def list_comments(db: Session, script_id: uuid.UUID) -> list[Comment]:
    return comment_repository.list_for_script(db, script_id)


def add_reply(db: Session, *, comment_id: uuid.UUID, author_id: uuid.UUID, content: str) -> CommentReply:
    reply = comment_repository.add_reply(db, comment_id=comment_id, author_id=author_id, content=content)
    db.commit()
    db.refresh(reply)
    return reply


def set_resolved(db: Session, comment: Comment, resolved: bool) -> Comment:
    updated = comment_repository.set_resolved(db, comment, resolved)
    db.commit()
    db.refresh(updated)
    return updated
