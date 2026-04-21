from dataclasses import dataclass

from app.domain.entities.ticket import Ticket
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_status import TicketStatus
from app.domain.exceptions.ticket_exceptions import ClosedTicketUpdateError
from app.domain.repositories.ticket_repository import TicketRepository


@dataclass(slots=True)
class UpdateTicketInput:
    ticket_id: int
    category_id: int | None
    priority: TicketPriority | None
    status: TicketStatus | None


class UpdateTicketUseCase:
    def __init__(self, repository: TicketRepository) -> None:
        self._ticket_repository = repository

    def execute(self, input_data: UpdateTicketInput) -> Ticket:

        existing_ticket = self._ticket_repository.get_by_id(input_data.ticket_id)

        if existing_ticket.status == TicketStatus.OPEN:
            if input_data.category_id is not None:
                existing_ticket.category_id = input_data.category_id

            if input_data.priority is not None:
                existing_ticket.priority = input_data.priority

            if input_data.status is not None:
                existing_ticket.status = input_data.status

            return self._ticket_repository.update(existing_ticket)
        else:
            raise ClosedTicketUpdateError()
