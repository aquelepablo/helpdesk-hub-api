from fastapi.testclient import TestClient

from app.main import API_PREFIX
from tests.integration.factories import create_category


def test_get_ticket_by_id_returns_ticket_details(client: TestClient) -> None:
    category_id = create_category(client)

    created = client.post(
        f"{API_PREFIX}/tickets",
        json={
            "title": "Email bloqueado",
            "description": "Nao recebe mensagens externas",
            "category_id": category_id,
            "priority": "medium",
        },
    ).json()

    ticket_id = created["data"]["id"]

    response = client.get(f"{API_PREFIX}/tickets/{ticket_id}")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["id"] == ticket_id
    assert body["data"]["title"] == "Email bloqueado"


def test_get_ticket_by_id_returns_not_found_for_unknown_id(client: TestClient) -> None:
    invalid_ticket_id = 999

    response = client.get(f"{API_PREFIX}/tickets/{invalid_ticket_id}")
    body = response.json()

    assert response.status_code == 404
    assert body["success"] is False
    assert body["message"] == f"Ticket with id {invalid_ticket_id} was not found."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    error_codes = {error["code"] for error in body["details"]["errors"]}

    assert "not_found" in error_codes
