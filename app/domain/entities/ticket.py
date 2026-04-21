from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_status import TicketStatus


@dataclass(slots=True)
class Ticket:
    id: int = 0
    title: str = ""
    description: str = ""
    category_id: int = 0
    priority: TicketPriority = TicketPriority.LOW
    status: TicketStatus = TicketStatus.OPEN
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
