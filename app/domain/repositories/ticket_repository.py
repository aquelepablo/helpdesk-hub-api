from abc import ABC, abstractmethod

from app.domain.entities.ticket import Ticket


class TicketRepository(ABC):
    @abstractmethod
    def create(self, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Ticket]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int) -> Ticket:
        raise NotImplementedError

    @abstractmethod
    def update(self, updated_ticket: Ticket) -> Ticket:
        raise NotImplementedError
