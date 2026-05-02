from dataclasses import dataclass

from app.application.interfaces.repositories.category_repository import (
    ICategoryRepository,
)
from app.application.interfaces.repositories.ticket_repository import (
    ITicketRepository,
)
from app.domain.entities.ticket import Ticket
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_status import TicketStatus
from app.domain.exceptions.ticket_exceptions import ClosedTicketUpdateError


@dataclass(slots=True)
class UpdateTicketInput:
    ticket_id: int
    category_id: int | None = None
    priority: TicketPriority | None = None
    status: TicketStatus | None = None


class UpdateTicketUseCase:
    def __init__(
        self,
        ticket_repository: ITicketRepository,
        category_repository: ICategoryRepository,
    ) -> None:
        self._ticket_repo = ticket_repository
        self._category_repo = category_repository

    def execute(self, input_data: UpdateTicketInput) -> Ticket:

        existing_ticket = self._ticket_repo.get_by_id(input_data.ticket_id)

        if not existing_ticket.status == TicketStatus.OPEN:
            raise ClosedTicketUpdateError()

        if input_data.category_id is not None:
            self._category_repo.get_by_id(input_data.category_id)
            existing_ticket.category_id = input_data.category_id

        if input_data.priority is not None:
            existing_ticket.priority = input_data.priority

        if input_data.status is not None:
            existing_ticket.status = input_data.status

        return self._ticket_repo.update(existing_ticket)
