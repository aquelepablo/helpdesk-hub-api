from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.sqlalchemy.database import Base

if TYPE_CHECKING:
    from app.infrastructure.db.sqlalchemy.models import TicketORM


class CategoryORM(Base):
    __tablename__ = "categories"

    # Columns
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
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
    tickets: Mapped[list["TicketORM"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return (
            f"<CategoryORM(id={self.id}, title={self.name}, status={self.is_active})>"
        )
