from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.sqlalchemy.database import Base

if TYPE_CHECKING:
    from app.infrastructure.db.sqlalchemy.models import TicketORM


class CommentORM(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_internal: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    ticket: Mapped["TicketORM"] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return f"<CommentORM(id={self.id}, ticket_id={self.ticket_id})>"
