import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.infrastructure.db.repositories.memory.memory_database import (
    category_db,
    comment_db,
    ticket_db,
)

load_dotenv()

# 2) pega a URL original
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL não configurada.")

# 3) cria a URL da base de teste
test_database_url = database_url.rsplit("/", 1)[0] + "/helpdesk_db_test"

# 4) sobrescreve para os testes
os.environ["DATABASE_URL"] = test_database_url

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


@pytest.fixture(autouse=True)
def truncate_database() -> Generator[None, None, None]:
    if not str(engine.url).endswith("helpdesk_db_test"):
        raise RuntimeError(
            f"Testes tentando limpar uma base que não é de teste: {engine.url}"
        )

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client
