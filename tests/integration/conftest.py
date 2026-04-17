import pytest

from app.infra.db.repositories.memory_database import category_db, ticket_db


@pytest.fixture(autouse=True)
def reset_memory() -> None:
    category_db.id_counter = 0
    category_db.categories.clear()
    ticket_db.id_counter = 0
    ticket_db.tickets.clear()
