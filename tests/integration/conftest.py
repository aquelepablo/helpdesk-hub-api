import pytest

from app.infrastructure.db.repositories.memory_database import (
    category_db,
    comment_db,
    ticket_db,
)


@pytest.fixture(autouse=True)
def reset_memory() -> None:
    category_db.id_counter = 0
    category_db.categories.clear()
    ticket_db.id_counter = 0
    ticket_db.tickets.clear()
    comment_db.id_counter = 0
    comment_db.comments.clear()
