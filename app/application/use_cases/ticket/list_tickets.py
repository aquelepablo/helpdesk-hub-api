from app.application.use_cases.ticket.repository.ticket_repository import (
    TicketRepository,
)
from app.domain.entities.ticket import Ticket


class ListTicketsUseCase:
    def __init__(self, ticket_repository: TicketRepository) -> None:
        self._ticket_repository = ticket_repository

    def execute(self) -> list[Ticket]:

        tickets = self._ticket_repository.list_all()

        return tickets
