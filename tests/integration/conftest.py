import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.infrastructure.db.repositories.memory.memory_database import (
    category_db,
    comment_db,
    ticket_db,
)

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL não configurada.")

os.environ["DATABASE_URL"] = database_url + "_test"
os.environ["ENVIRONMENT"] = "test"

from app.infrastructure.db.sqlalchemy.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def reset_memory() -> None:
    category_db.id_counter = 0
    category_db.categories.clear()
    ticket_db.id_counter = 0
    ticket_db.tickets.clear()
    comment_db.id_counter = 0
    comment_db.comments.clear()


@pytest.fixture(scope="session", autouse=True)
def prepare_database_schema() -> Generator[None, None, None]:
    if not str(engine.url).endswith("_test"):
        raise RuntimeError(
            f"Testes tentando limpar uma base que não é de teste: {engine.url}"
        )

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


def clear_database() -> None:
    with engine.begin() as connection:
        connection.execute(
            text("TRUNCATE comments, tickets, categories RESTART IDENTITY CASCADE")
        )


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        clear_database()
        yield test_client
