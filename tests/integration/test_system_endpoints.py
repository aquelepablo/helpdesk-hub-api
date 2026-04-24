from fastapi.testclient import TestClient

from app.infrastructure.settings.settings import settings
from app.main import API_PREFIX, app

client = TestClient(app)


def test_get_root_returns_service_metadata() -> None:
    response = client.get(API_PREFIX)

    assert response.status_code == 200
    assert response.json() == {
        "service": settings.app_title,
        "description": settings.app_description,
    }


def test_get_liveness_returns_ok() -> None:
    response = client.get(f"{API_PREFIX}/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_health_returns_structured_payload() -> None:
    response = client.get(f"{API_PREFIX}/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "checks": [],
    }


def test_get_info_returns_application_metadata() -> None:
    response = client.get(f"{API_PREFIX}/info")

    assert response.status_code == 200
    assert response.json() == {
        "service": settings.app_title,
        "project_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env.value,
    }


def test_get_ping_returns_utc_timestamp() -> None:
    response = client.get(f"{API_PREFIX}/ping")

    assert response.status_code == 200
    body = response.json()

    assert "timestamp" in body
    assert body["timezone"] == "UTC"
    assert body["timestamp"].endswith("+00:00")
