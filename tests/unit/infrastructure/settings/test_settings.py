from pathlib import Path

import pytest
from pydantic import ValidationError

from app.infrastructure.settings.settings import AppEnv, Settings


def test_settings_reads_database_url_from_env_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("PORT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("RUN_POSTGRES_TESTS", raising=False)

    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "PROJECT_NAME=helpdesk-hub-api",
                "PROJECT_TITLE=HelpDesk Hub API",
                "PROJECT_DESCRIPTION=API de gestão de chamados",
                "PROJECT_VERSION=0.1.0",
                "ENVIRONMENT=development",
                "PORT=8000",
                "LOG_LEVEL=INFO",
                "DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/helpdesk_db",
            ]
        ),
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)  # pyright: ignore[reportCallIssue]

    assert (
        settings.database_url
        == "postgresql+psycopg://user:password@localhost:5432/helpdesk_db"
    )


def test_settings_requires_database_url(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("PORT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "PROJECT_NAME=helpdesk-hub-api",
                "PROJECT_TITLE=HelpDesk Hub API",
                "PROJECT_DESCRIPTION=API de gestão de chamados",
                "PROJECT_VERSION=0.1.0",
                "ENVIRONMENT=development",
                "PORT=8000",
                "LOG_LEVEL=INFO",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        Settings(_env_file=env_file)  # pyright: ignore[reportCallIssue]


def test_settings_reads_runtime_values_from_env_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.delenv("PORT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)

    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "PROJECT_NAME=helpdesk-hub-api",
                "PROJECT_TITLE=HelpDesk Hub API",
                "PROJECT_DESCRIPTION=API de gestão de chamados",
                "PROJECT_VERSION=0.1.0",
                "ENVIRONMENT=test",
                "PORT=9000",
                "LOG_LEVEL=DEBUG",
                "DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/helpdesk_db",
                "RUN_POSTGRES_TESTS=true",
            ]
        ),
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)  # pyright: ignore[reportCallIssue]

    assert settings.environment == AppEnv.TEST
    assert settings.port == 9000
    assert settings.log_level == "DEBUG"
    assert settings.run_postgres_tests is True
