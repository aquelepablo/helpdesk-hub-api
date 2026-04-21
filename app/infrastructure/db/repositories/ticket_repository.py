import copy
from datetime import UTC, datetime

from app.domain.entities.ticket import Ticket, TicketFilter
from app.domain.exceptions.ticket_exceptions import TicketNotFoundError
from app.infrastructure.db.repositories.memory_database import ticket_db


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

    def save(self, ticket: Ticket) -> Ticket:
        if ticket.id is None:
            return self._create(ticket)
        else:
            return self._update(ticket.id, ticket)

    def list_by_filter(self, ticket_filter: TicketFilter) -> list[Ticket]:

        has_no_filters = all(
            value is None
            for value in (
                ticket_filter.status,
                ticket_filter.priority,
                ticket_filter.category_id,
            )
        )

        if has_no_filters:
            return copy.deepcopy(ticket_db.tickets)

        tickets: list[Ticket] = []

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

        return copy.deepcopy(tickets)

    def get_by_id(self, ticket_id: int) -> Ticket:
        stored_ticket = self._find_stored_ticket_by_id(ticket_id)
        return copy.deepcopy(stored_ticket)
