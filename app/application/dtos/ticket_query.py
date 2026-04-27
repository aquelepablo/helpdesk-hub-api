from dataclasses import dataclass, field

from app.application.dtos.sorting import OrderCriterion, SortDirection
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_sort_field import TicketSortField
from app.domain.enum.ticket_status import TicketStatus


@dataclass(slots=True)
class TicketFilter:
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    category_id: int | None = None
    sort_order: OrderCriterion = field(
        default_factory=lambda: OrderCriterion(TicketSortField.ID, SortDirection.ASC)
    )
