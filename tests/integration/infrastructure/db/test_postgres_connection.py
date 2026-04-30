import psycopg
import pytest

from app.infrastructure.settings.settings import settings


def test_postgres_database_is_accessible() -> None:
    if not settings.run_postgres_tests:
        pytest.skip("PostgreSQL integration test disabled")

    with (
        psycopg.connect(settings.database_url) as connection,
        connection.cursor() as cursor,
    ):
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

    assert result == (1,)
