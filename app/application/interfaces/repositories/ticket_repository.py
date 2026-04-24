from typing import Protocol

from app.application.dtos.pagination import PagedResult, PaginationParams
from app.application.dtos.ticket_query import TicketFilter
from app.domain.entities.ticket import Ticket


class TicketRepository(Protocol):
    def save(self, ticket: Ticket) -> Ticket: ...

    def list_by_filter(
        self, ticket_filter: TicketFilter, pagination_params: PaginationParams
    ) -> PagedResult[Ticket]: ...

    def get_by_id(self, ticket_id: int) -> Ticket: ...
