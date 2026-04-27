from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True, kw_only=True)
class Comment:
    id: int | None = None
    ticket_id: int
    content: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
