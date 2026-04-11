import copy
from datetime import datetime

from app.domain.entities.ticket import Ticket
from app.domain.repositories.ticket_repository import TicketRepository
from app.infra.db.repositories.memory_database import ticket_db


class InMemoryTicketRepository(TicketRepository):
    def create(self, ticket: Ticket) -> Ticket:
        ticket_db.id_counter += 1
        ticket.id = ticket_db.id_counter

        ticket.created_at = datetime.now()
        ticket.updated_at = datetime.now()

        ticket_db.add(ticket)

        return ticket

    def list_all(self) -> list[Ticket]:
        return copy.deepcopy(ticket_db.tickets)

    def get_by_id(self, id: int) -> Ticket:
        for ticket in ticket_db.tickets:
            if ticket.id == id:
                return copy.deepcopy(ticket)

        raise ValueError(f"Ticket {id} não encontrado.")

    def update(self, updated_ticket: Ticket) -> Ticket:
        stored_ticket = self.get_by_id(updated_ticket.id)

        stored_ticket.title = updated_ticket.title
        stored_ticket.description = updated_ticket.description
        stored_ticket.category_id = updated_ticket.category_id
        stored_ticket.priority = updated_ticket.priority
        stored_ticket.status = updated_ticket.status
        stored_ticket.updated_at = datetime.now()

        return copy.deepcopy(stored_ticket)
