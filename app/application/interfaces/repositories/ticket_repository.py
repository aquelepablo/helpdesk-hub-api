from abc import ABC, abstractmethod

from app.application.dtos.pagination import PagedResult, PaginationParams
from app.application.dtos.ticket_query import TicketFilter
from app.domain.entities.ticket import Ticket


class ITicketRepository(ABC):
    @abstractmethod
    def create(self, ticket: Ticket) -> Ticket: ...

    @abstractmethod
    def update(self, updated_ticket: Ticket) -> Ticket: ...

    @abstractmethod
    def list_by_filter(
        self, ticket_filter: TicketFilter, pagination_params: PaginationParams
    ) -> PagedResult[Ticket]: ...

    @abstractmethod
    def get_by_id(self, ticket_id: int) -> Ticket: ...
