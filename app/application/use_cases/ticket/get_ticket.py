from app.application.interfaces.repositories.ticket_repository import (
    ITicketRepository,
)
from app.domain.entities.ticket import Ticket


class GetTicketUseCase:
    def __init__(self, ticket_repository: ITicketRepository) -> None:
        self._ticket_repository = ticket_repository

    def execute(self, ticket_id: int) -> Ticket:

        ticket = self._ticket_repository.get_by_id(ticket_id)

        return ticket
