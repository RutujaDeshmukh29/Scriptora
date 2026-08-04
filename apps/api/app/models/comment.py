import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.comment_reply import CommentReply
    from app.models.script import Script
    from app.models.user import User


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    script_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("scripts.id", ondelete="CASCADE"), nullable=False
    )
    author_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Anchors the comment to a text range in the editor at the moment it was
    # created. These are raw ProseMirror positions, so they can drift once a
    # document changes a lot — quoted_text preserves *what* was commented on
    # even if the position no longer lines up exactly. True stable anchoring
    # arrives with Yjs-based collaboration in Phase 2.
    anchor_from: Mapped[int | None] = mapped_column(Integer, nullable=True)
    anchor_to: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quoted_text: Mapped[str | None] = mapped_column(String(500), nullable=True)

    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    script: Mapped["Script"] = relationship()
    author: Mapped["User"] = relationship()
    replies: Mapped[list["CommentReply"]] = relationship(
        back_populates="comment", cascade="all, delete-orphan", order_by="CommentReply.created_at"
    )

    def __repr__(self) -> str:
        return f"<Comment id={self.id} script_id={self.script_id} resolved={self.resolved}>"
