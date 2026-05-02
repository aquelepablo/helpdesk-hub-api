from fastapi.testclient import TestClient

from app.main import API_PREFIX
from tests.integration.factories import create_category


def test_update_ticket_returns_updated_ticket(client: TestClient) -> None:
    category_id = create_category(client)

    created = client.post(
        f"{API_PREFIX}/tickets",
        json={
            "title": "VPN instável",
            "description": "Conexão cai durante o expediente",
            "category_id": category_id,
            "priority": "low",
        },
    ).json()

    ticket_id = created["data"]["id"]

    response = client.patch(
        f"{API_PREFIX}/tickets/{ticket_id}",
        json={
            "priority": "urgent",
            "status": "closed",
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["priority"] == "urgent"
    assert body["data"]["status"] == "closed"


def test_update_ticket_returns_not_found_for_unknown_id(client: TestClient) -> None:
    invalid_ticket_id = 999

    response = client.patch(
        f"{API_PREFIX}/tickets/{invalid_ticket_id}",
        json={
            "priority": "urgent",
            "status": "closed",
        },
    )
    body = response.json()

    assert response.status_code == 404
    assert body["success"] is False
    assert body["message"] == f"Ticket with id {invalid_ticket_id} was not found."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    error_codes = {error["code"] for error in body["details"]["errors"]}

    assert "not_found" in error_codes
