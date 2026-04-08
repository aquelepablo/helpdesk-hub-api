from fastapi.testclient import TestClient

from app.infra.settings.project_metadata import project_metadata
from app.infra.settings.settings import settings
from app.main import app

client = TestClient(app)


def test_get_root_returns_service_metadata() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "service": project_metadata.title,
        "description": project_metadata.description,
    }


def test_get_liveness_returns_ok() -> None:
    response = client.get("/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_health_returns_structured_payload() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "checks": [],
    }


def test_get_info_returns_application_metadata() -> None:
    response = client.get("/info")

    assert response.status_code == 200
    assert response.json() == {
        "service": project_metadata.title,
        "project_name": project_metadata.name,
        "version": project_metadata.version,
        "environment": settings.app_env.value,
    }


def test_get_ping_returns_utc_timestamp() -> None:
    response = client.get("/ping")

    assert response.status_code == 200
    body = response.json()

    assert "timestamp" in body
    assert body["timezone"] == "UTC"
    assert body["timestamp"].endswith("+00:00")
