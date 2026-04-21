from dataclasses import dataclass

from app.application.ports.ticket_repository import (
    TicketRepository,
)
from app.domain.entities.ticket import Ticket, TicketFilter
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_status import TicketStatus


@dataclass(slots=True)
class ListTicketsInput:
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    category_id: int | None = None


class ListTicketsUseCase:
    def __init__(self, ticket_repository: TicketRepository) -> None:
        self._ticket_repository = ticket_repository

    def execute(self, input_data: ListTicketsInput) -> list[Ticket]:

        ticket_filter = TicketFilter(
            status=input_data.status,
            priority=input_data.priority,
            category_id=input_data.category_id,
        )

        tickets = self._ticket_repository.list_by_filter(ticket_filter)

        return tickets
