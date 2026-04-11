from app.domain.entities.ticket import Ticket
from app.domain.repositories.ticket_repository import TicketRepository


class GetTicketByIdUseCase:
    def __init__(self, repository: TicketRepository) -> None:
        self.ticket_repository = repository

    def execute(self, ticket_id: int) -> Ticket:

        ticket = self.ticket_repository.get_by_id(ticket_id)

        return ticket
