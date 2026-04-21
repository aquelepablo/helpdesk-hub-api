from typing import Protocol

from app.domain.entities.ticket import Ticket, TicketFilter


class TicketRepository(Protocol):
    def save(self, ticket: Ticket) -> Ticket: ...

    def list_by_filter(self, filter: TicketFilter) -> list[Ticket]: ...

    def get_by_id(self, ticket_id: int) -> Ticket: ...
