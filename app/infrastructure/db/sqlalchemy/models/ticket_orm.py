from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_status import TicketStatus
from app.infrastructure.db.sqlalchemy.database import Base

if TYPE_CHECKING:
    from app.infrastructure.db.sqlalchemy.models import CategoryORM


def enum_values(enum_class: type[StrEnum]) -> list[str]:
    return [item.value for item in enum_class]


class TicketORM(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    priority: Mapped[TicketPriority] = mapped_column(
        SqlEnum(
            TicketPriority,
            values_callable=enum_values,
            name="ticket_priority",
        ),
        nullable=False,
        default=TicketPriority.LOW,
    )
    status: Mapped[TicketStatus] = mapped_column(
        SqlEnum(
            TicketStatus,
            values_callable=enum_values,
            name="ticket_status",
        ),
        nullable=False,
        default=TicketStatus.OPEN,
    )
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

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
    )

    category: Mapped["CategoryORM"] = relationship(back_populates="tickets")

    def __repr__(self) -> str:
        return f"<TicketORM(id={self.id}, title={self.title}, status={self.status})>"
