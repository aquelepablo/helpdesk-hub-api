from dataclasses import dataclass

from app.application.interfaces.repositories.category_repository import (
    CategoryRepository,
)
from app.application.interfaces.repositories.ticket_repository import (
    TicketRepository,
)
from app.domain.entities.ticket import Ticket
from app.domain.enum.ticket_priority import TicketPriority


@dataclass(slots=True)
class CreateTicketInput:
    title: str
    description: str
    category_id: int
    priority: TicketPriority


class CreateTicketUseCase:
    def __init__(
        self,
        ticket_repository: TicketRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._ticket_repo = ticket_repository
        self._category_repo = category_repository

    def execute(self, input_data: CreateTicketInput) -> Ticket:

        self._category_repo.get_by_id(input_data.category_id)

        new_ticket = Ticket(
            title=input_data.title,
            description=input_data.description,
            category_id=input_data.category_id,
            priority=input_data.priority,
        )

        persisted_ticket: Ticket = self._ticket_repo.save(new_ticket)

        return persisted_ticket
