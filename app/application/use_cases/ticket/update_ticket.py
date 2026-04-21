from dataclasses import dataclass

from app.application.ports.category_repository import (
    CategoryRepository,
)
from app.application.ports.ticket_repository import (
    TicketRepository,
)
from app.domain.entities.ticket import Ticket
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_status import TicketStatus
from app.domain.exceptions.ticket_exceptions import ClosedTicketUpdateError


@dataclass(slots=True)
class UpdateTicketInput:
    category_id: int | None
    priority: TicketPriority | None
    status: TicketStatus | None


class UpdateTicketUseCase:
    def __init__(
        self,
        ticket_repository: TicketRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._ticket_repo = ticket_repository
        self._category_repo = category_repository

    def execute(self, ticket_id: int, input_data: UpdateTicketInput) -> Ticket:

        existing_ticket = self._ticket_repo.get_by_id(ticket_id)

        if not existing_ticket.status == TicketStatus.OPEN:
            raise ClosedTicketUpdateError()

        if input_data.category_id is not None:
            self._category_repo.get_by_id(input_data.category_id)
            existing_ticket.category_id = input_data.category_id

        if input_data.priority is not None:
            existing_ticket.priority = input_data.priority

        if input_data.status is not None:
            existing_ticket.status = input_data.status

        return self._ticket_repo.save(existing_ticket)
