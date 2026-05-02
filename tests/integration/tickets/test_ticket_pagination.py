from fastapi.testclient import TestClient

from app.main import API_PREFIX
from tests.integration.factories import create_category, create_ticket


def test_list_tickets_returns_paginated_tickets(client: TestClient) -> None:
    category_id = create_category(client)

    first_ticket_id = create_ticket(
        client,
        title="Ticket 1",
        category_id=category_id,
        priority="low",
    )
    second_ticket_id = create_ticket(
        client,
        title="Ticket 2",
        category_id=category_id,
        priority="medium",
    )
    third_ticket_id = create_ticket(
        client,
        title="Ticket 3",
        category_id=category_id,
        priority="high",
    )

    response = client.get(
        f"{API_PREFIX}/tickets",
        params={"page": 2, "page_size": 2},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Tickets listados com sucesso"
    assert body["total_items"] == 3
    assert body["page"] == 2
    assert body["page_size"] == 2
    assert body["total_pages"] == 2
    assert len(body["items"]) == 1
    assert body["items"][0]["id"] == third_ticket_id
    assert body["items"][0]["id"] not in (first_ticket_id, second_ticket_id)
