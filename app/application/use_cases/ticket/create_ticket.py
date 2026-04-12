from dataclasses import dataclass

from app.domain.entities.ticket import Ticket
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.repositories.ticket_repository import TicketRepository


@dataclass(slots=True)
class CreateTicketInput:
    title: str
    description: str
    category_id: int
    priority: TicketPriority


class CreateTicketUseCase:
    def __init__(self, repository: TicketRepository) -> None:
        self._ticket_repository = repository

    def execute(self, input_data: CreateTicketInput) -> Ticket:

        new_ticket = Ticket(
            title=input_data.title,
            description=input_data.description,
            category_id=input_data.category_id,
            priority=input_data.priority,
        )

        persisted_ticket = self._ticket_repository.create(new_ticket)

        return persisted_ticket
