from fastapi.testclient import TestClient

from app.main import API_PREFIX
from tests.integration.factories import create_category, create_ticket


def test_list_tickets_ordered_by_id_descending(client: TestClient) -> None:
    hardware_category_id = create_category(client)
    software_category_id = create_category(
        client, "Software", "Categoria para sistemas", True
    )

    create_ticket(
        client,
        title="Mouse quebrado",
        category_id=hardware_category_id,
        priority="high",
    )
    create_ticket(
        client,
        title="ERP lento",
        category_id=software_category_id,
        priority="high",
    )
    third_ticket_id = create_ticket(
        client,
        title="Editor travando",
        category_id=software_category_id,
        priority="low",
    )

    response = client.get(
        f"{API_PREFIX}/tickets",
        params={"sort_direction": "desc"},
    )
    body = response.json()

    assert response.status_code == 200
    assert len(body["items"]) == 3
    assert body["items"][0]["id"] == third_ticket_id
    assert body["items"][0]["category_id"] == software_category_id
    assert body["items"][0]["priority"] == "low"


def test_list_tickets_ordered_by_priority_descending(client: TestClient) -> None:
    hardware_category_id = create_category(client)
    software_category_id = create_category(
        client, "Software", "Categoria para sistemas", True
    )

    create_ticket(
        client,
        title="Mouse quebrado",
        category_id=hardware_category_id,
        priority="high",
    )
    create_ticket(
        client,
        title="ERP lento",
        category_id=software_category_id,
        priority="medium",
    )
    last_expected_ticket_id = create_ticket(
        client,
        title="Editor travando",
        category_id=software_category_id,
        priority="low",
    )
    first_expected_ticket_id = create_ticket(
        client,
        title="Sistema offline",
        category_id=software_category_id,
        priority="urgent",
    )

    response = client.get(
        f"{API_PREFIX}/tickets",
        params={"sort_field": "priority", "sort_direction": "desc"},
    )
    body = response.json()

    assert response.status_code == 200
    assert len(body["items"]) == 4
    assert body["items"][0]["id"] == first_expected_ticket_id
    assert body["items"][0]["category_id"] == software_category_id
    assert body["items"][0]["priority"] == "urgent"
    assert body["items"][3]["id"] == last_expected_ticket_id
    assert body["items"][3]["category_id"] == software_category_id
    assert body["items"][3]["priority"] == "low"
