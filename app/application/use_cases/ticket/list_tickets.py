from app.domain.entities.ticket import Ticket
from app.domain.repositories.ticket_repository import TicketRepository


class ListTicketsUseCase:
    def __init__(self, repository: TicketRepository) -> None:
        self.ticket_repository = repository

    def execute(self) -> list[Ticket]:

        tickets = self.ticket_repository.list_all()

        return tickets
