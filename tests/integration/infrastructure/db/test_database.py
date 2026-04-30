import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.infrastructure.db.sqlalchemy.database import get_db_session
from app.infrastructure.settings.settings import settings


def test_get_db_session_yields_sqlalchemy_session() -> None:
    session_generator = get_db_session()
    session = next(session_generator)

    try:
        assert isinstance(session, Session)
    finally:
        session_generator.close()


def test_postgres_database_is_accessible() -> None:
    if not settings.run_postgres_tests:
        pytest.skip("PostgreSQL integration test disabled")

    session_generator = get_db_session()

    try:
        session = next(session_generator)
        result = session.execute(text("SELECT 1")).scalar_one()
    finally:
        session_generator.close()

    assert result == 1
