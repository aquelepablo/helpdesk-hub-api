from fastapi.testclient import TestClient

from app.main import API_PREFIX
from tests.integration.factories import create_category


def test_create_ticket_returns_created_ticket(client: TestClient) -> None:
    category_id = create_category(client)

    payload: dict[str, str | int] = {
        "title": "Notebook sem acesso",
        "description": "Usuário nao consegue entrar no equipamento",
        "category_id": category_id,
        "priority": "high",
    }

    response = client.post(f"{API_PREFIX}/tickets", json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body["success"] is True
    assert body["message"] == "Ticket criado com sucesso"
    assert body["data"]["id"] == 1
    assert body["data"]["title"] == "Notebook sem acesso"
    assert body["data"]["category_id"] == category_id
    assert body["data"]["priority"] == "high"


def test_create_ticket_returns_422_for_invalid_payload(client: TestClient) -> None:
    response = client.post(
        f"{API_PREFIX}/tickets",
        json={
            "title": "Impressora sem toner",
            "category_id": 999,
            "priority": "invalid_priority",
        },
    )
    body = response.json()

    assert response.status_code == 422
    assert body["success"] is False
    assert body["message"] == "Request validation failed."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    error_fields = {error["field"] for error in body["details"]["errors"]}

    assert "description" in error_fields
    assert "priority" in error_fields
