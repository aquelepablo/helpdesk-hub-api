from app.application.use_cases.ticket.repository.ticket_repository import (
    TicketRepository,
)
from app.domain.entities.ticket import Ticket


class GetTicketByIdUseCase:
    def __init__(self, repository: TicketRepository) -> None:
        self._ticket_repository = repository

    def execute(self, ticket_id: int) -> Ticket:

        ticket = self._ticket_repository.get_by_id(ticket_id)

        return ticket
