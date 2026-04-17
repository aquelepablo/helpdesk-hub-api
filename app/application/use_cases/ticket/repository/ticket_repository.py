from typing import Protocol

from app.domain.entities.ticket import Ticket


class TicketRepository(Protocol):
    def save(self, ticket: Ticket) -> Ticket: ...

    def list_all(self) -> list[Ticket]: ...

    def get_by_id(self, ticket_id: int) -> Ticket: ...
