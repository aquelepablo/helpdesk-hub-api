from fastapi.testclient import TestClient

from app.main import API_PREFIX
from tests.integration.factories import create_category, create_ticket


def test_list_tickets_filters_by_status(client: TestClient) -> None:
    category_id = create_category(client)
    open_ticket_id = create_ticket(
        client,
        title="Monitor sem imagem",
        category_id=category_id,
        priority="low",
    )
    closed_ticket_id = create_ticket(
        client,
        title="VPN indisponível",
        category_id=category_id,
        priority="high",
    )

    client.patch(
        f"{API_PREFIX}/tickets/{closed_ticket_id}",
        json={"status": "closed"},
    )

    response = client.get(f"{API_PREFIX}/tickets", params={"status": "open"})
    body = response.json()

    assert response.status_code == 200
    assert len(body["items"]) == 1
    assert body["items"][0]["id"] == open_ticket_id
    assert body["items"][0]["status"] == "open"


def test_list_tickets_filters_by_priority(client: TestClient) -> None:
    category_id = create_category(client)
    create_ticket(
        client,
        title="Teclado com falha",
        category_id=category_id,
        priority="low",
    )
    high_priority_ticket_id = create_ticket(
        client,
        title="Sistema financeiro fora",
        category_id=category_id,
        priority="high",
    )

    response = client.get(f"{API_PREFIX}/tickets", params={"priority": "high"})
    body = response.json()

    assert response.status_code == 200
    assert len(body["items"]) == 1
    assert body["items"][0]["id"] == high_priority_ticket_id
    assert body["items"][0]["priority"] == "high"


def test_list_tickets_filters_by_category(client: TestClient) -> None:
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
    expected_ticket_id = create_ticket(
        client,
        title="ERP lento",
        category_id=software_category_id,
        priority="high",
    )

    response = client.get(
        f"{API_PREFIX}/tickets", params={"category_id": software_category_id}
    )
    body = response.json()

    assert response.status_code == 200
    assert len(body["items"]) == 1
    assert body["items"][0]["id"] == expected_ticket_id
    assert body["items"][0]["priority"] == "high"


def test_list_tickets_filters_by_category_and_priority(client: TestClient) -> None:
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
    expected_ticket_id = create_ticket(
        client,
        title="ERP lento",
        category_id=software_category_id,
        priority="high",
    )
    create_ticket(
        client,
        title="Editor travando",
        category_id=software_category_id,
        priority="low",
    )

    response = client.get(
        f"{API_PREFIX}/tickets",
        params={
            "category_id": software_category_id,
            "priority": "high",
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert len(body["items"]) == 1
    assert body["items"][0]["id"] == expected_ticket_id
    assert body["items"][0]["category_id"] == software_category_id
    assert body["items"][0]["priority"] == "high"
