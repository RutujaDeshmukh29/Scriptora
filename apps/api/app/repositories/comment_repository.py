import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.comment import Comment
from app.models.comment_reply import CommentReply


def create_comment(
    db: Session,
    *,
    script_id: uuid.UUID,
    author_id: uuid.UUID,
    content: str,
    anchor_from: int | None,
    anchor_to: int | None,
    quoted_text: str | None,
) -> Comment:
    comment = Comment(
        script_id=script_id,
        author_id=author_id,
        content=content,
        anchor_from=anchor_from,
        anchor_to=anchor_to,
        quoted_text=quoted_text,
    )
    db.add(comment)
    db.flush()
    return comment


def get_by_id(db: Session, comment_id: uuid.UUID) -> Comment | None:
    return db.get(Comment, comment_id)


def list_for_script(db: Session, script_id: uuid.UUID) -> list[Comment]:
    stmt = (
        select(Comment)
        .where(Comment.script_id == script_id)
        .options(joinedload(Comment.author), joinedload(Comment.replies).joinedload(CommentReply.author))
        .order_by(Comment.created_at)
    )
    # .unique() is required here: joinedload on a collection (replies)
    # duplicates the parent row once per child row.
    return list(db.execute(stmt).unique().scalars().all())


def add_reply(db: Session, *, comment_id: uuid.UUID, author_id: uuid.UUID, content: str) -> CommentReply:
    reply = CommentReply(comment_id=comment_id, author_id=author_id, content=content)
    db.add(reply)
    db.flush()
    return reply


def set_resolved(db: Session, comment: Comment, resolved: bool) -> Comment:
    comment.resolved = resolved
    db.flush()
    return comment
