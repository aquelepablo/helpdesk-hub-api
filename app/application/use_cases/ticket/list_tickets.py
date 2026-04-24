from dataclasses import dataclass

from app.application.dtos.pagination import PagedResult, PaginationParams
from app.application.dtos.sorting import OrderCriterion, SortDirection
from app.application.dtos.ticket_query import TicketFilter
from app.application.interfaces.repositories.ticket_repository import (
    TicketRepository,
)
from app.domain.entities.ticket import Ticket
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_sort_field import TicketSortField
from app.domain.enum.ticket_status import TicketStatus


@dataclass(slots=True)
class ListTicketsInput:
    pagination_params: PaginationParams
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    category_id: int | None = None
    sort_field: TicketSortField = TicketSortField.ID
    sort_order: SortDirection = SortDirection.ASC


class ListTicketsUseCase:
    def __init__(self, ticket_repository: TicketRepository) -> None:
        self._ticket_repository = ticket_repository

    def execute(self, input_data: ListTicketsInput) -> PagedResult[Ticket]:

        ticket_filter = TicketFilter(
            status=input_data.status,
            priority=input_data.priority,
            category_id=input_data.category_id,
            sort_order=OrderCriterion(
                field=input_data.sort_field.value, direction=input_data.sort_order
            ),
        )

        tickets = self._ticket_repository.list_by_filter(
            ticket_filter, input_data.pagination_params
        )

        return tickets
