from app.domain.entities.category import Category
from app.domain.entities.ticket import Ticket


class CategoryDatabase:
    def __init__(self) -> None:
        self.id_counter = 0
        self.categories: list[Category] = []

    def add(self, category: Category) -> Category:
        self.categories.append(category)
        return category


class TicketDatabase:
    def __init__(self) -> None:
        self.id_counter = 0
        self.tickets: list[Ticket] = []

    def add(self, ticket: Ticket) -> Ticket:
        self.tickets.append(ticket)
        return ticket


category_db = CategoryDatabase()
ticket_db = TicketDatabase()
