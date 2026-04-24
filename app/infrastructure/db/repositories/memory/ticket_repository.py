import copy
from datetime import UTC, datetime
from math import ceil
from operator import attrgetter

from app.application.dtos.pagination import PagedResult, PaginationParams
from app.application.dtos.sorting import OrderCriterion, SortDirection
from app.application.dtos.ticket_query import TicketFilter
from app.domain.entities.ticket import Ticket
from app.domain.exceptions.ticket_exceptions import TicketNotFoundError
from app.infrastructure.db.repositories.memory.memory_database import ticket_db


class InMemoryTicketRepository:
    def _find_stored_ticket_by_id(self, ticket_id: int) -> Ticket:
        for ticket in ticket_db.tickets:
            if ticket.id == ticket_id:
                return ticket

        raise TicketNotFoundError(ticket_id)

    def _create(self, ticket: Ticket) -> Ticket:
        ticket_db.id_counter += 1
        ticket.id = ticket_db.id_counter

        ticket.created_at = datetime.now(UTC)
        ticket.updated_at = datetime.now(UTC)

        stored_ticket = ticket_db.add(ticket)

        return copy.deepcopy(stored_ticket)

    def _update(self, ticket_id: int, updated_ticket: Ticket) -> Ticket:
        stored_ticket = self._find_stored_ticket_by_id(ticket_id)

        stored_ticket.category_id = updated_ticket.category_id
        stored_ticket.priority = updated_ticket.priority
        stored_ticket.status = updated_ticket.status
        stored_ticket.updated_at = datetime.now(UTC)

        return copy.deepcopy(stored_ticket)

    def _sort_tickets_list(
        self, order_criterion: OrderCriterion, tickets_list: list[Ticket]
    ) -> list[Ticket]:
        sort_field = order_criterion.field
        reverse = order_criterion.direction == SortDirection.DESC

        sort_key_map = {
            "id": "id",
            "title": "title",
            "status": "status_sort_key",
            "priority": "priority_sort_key",
        }

        sorted_tickets = sorted(
            tickets_list, key=attrgetter(sort_key_map[sort_field]), reverse=reverse
        )

        return sorted_tickets

    def _filter_ticket_list(self, ticket_filter: TicketFilter) -> list[Ticket]:

        tickets: list[Ticket] = []

        has_no_filters = all(
            value is None
            for value in (
                ticket_filter.status,
                ticket_filter.priority,
                ticket_filter.category_id,
            )
        )

        if has_no_filters:
            tickets = ticket_db.tickets

        else:
            for ticket in ticket_db.tickets:
                if (
                    ticket_filter.status is not None
                    and ticket.status != ticket_filter.status
                ):
                    continue

                if (
                    ticket_filter.priority is not None
                    and ticket.priority != ticket_filter.priority
                ):
                    continue

                if (
                    ticket_filter.category_id is not None
                    and ticket.category_id != ticket_filter.category_id
                ):
                    continue

                tickets.append(ticket)

        sorted_tickets = self._sort_tickets_list(ticket_filter.sort_order, tickets)

        return sorted_tickets

    def save(self, ticket: Ticket) -> Ticket:
        if ticket.id is None:
            return self._create(ticket)
        else:
            return self._update(ticket.id, ticket)

    # TODO: split responsibilities
    def list_by_filter(
        self, ticket_filter: TicketFilter, pagination_params: PaginationParams
    ) -> PagedResult[Ticket]:

        tickets = self._filter_ticket_list(ticket_filter)

        total_items = len(tickets)
        start = pagination_params.offset
        end = pagination_params.offset + pagination_params.page_size
        paginated_tickets = tickets[start:end]
        total_pages = (
            ceil(total_items / pagination_params.page_size) if total_items else 0
        )

        return PagedResult(
            items=copy.deepcopy(paginated_tickets),
            total_items=total_items,
            page=pagination_params.page,
            page_size=pagination_params.page_size,
            total_pages=total_pages,
        )

    def get_by_id(self, ticket_id: int) -> Ticket:
        stored_ticket = self._find_stored_ticket_by_id(ticket_id)
        return copy.deepcopy(stored_ticket)
