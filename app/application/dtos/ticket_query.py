from dataclasses import dataclass

from app.application.dtos.sorting import SortDirection
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_sort_field import TicketSortField
from app.domain.enum.ticket_status import TicketStatus


@dataclass(slots=True)
class TicketFilter:
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    category_id: int | None = None
    sort_field: TicketSortField = TicketSortField.ID
    sort_direction: SortDirection = SortDirection.DESC
