from fastapi.testclient import TestClient

from app.main import API_PREFIX


def _create_category(
    client: TestClient,
    name: str = "Hardware",
    description: str = "Categoria para testes",
    is_active: bool = True,
) -> int:
    response = client.post(
        f"{API_PREFIX}/categories",
        json={
            "name": name,
            "description": description,
            "is_active": is_active,
        },
    )
    body = response.json()
    return int(body["data"]["id"])


def _create_ticket(
    client: TestClient,
    title: str,
    category_id: int,
    priority: str,
) -> int:
    response = client.post(
        f"{API_PREFIX}/tickets",
        json={
            "title": title,
            "description": "Ticket criado para teste de filtro",
            "category_id": category_id,
            "priority": priority,
        },
    )

    assert response.status_code == 201, {
        "status_code": response.status_code,
        "body": response.json(),
    }

    return int(response.json()["data"]["id"])


def test_list_tickets_returns_empty_list_when_memory_is_empty(
    client: TestClient,
) -> None:
    response = client.get(f"{API_PREFIX}/tickets")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Tickets listados com sucesso",
        "items": [],
        "total_items": 0,
        "page": 1,
        "page_size": 10,
        "total_pages": 0,
    }


# TODO: add client reference on methods
def test_list_tickets_returns_paginated_tickets(client: TestClient) -> None:
    category_id = _create_category(client)

    first_ticket_id = _create_ticket(
        client,
        title="Ticket 1",
        category_id=category_id,
        priority="low",
    )
    second_ticket_id = _create_ticket(
        client,
        title="Ticket 2",
        category_id=category_id,
        priority="medium",
    )
    third_ticket_id = _create_ticket(
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


def test_create_ticket_returns_created_ticket(client: TestClient) -> None:
    category_id = _create_category(client)

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


def test_get_ticket_by_id_returns_ticket_details(client: TestClient) -> None:
    category_id = _create_category(client)

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


def test_update_ticket_returns_updated_ticket(client: TestClient) -> None:
    category_id = _create_category(client)

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


def test_create_ticket_returns_422_for_invalid_payload(client: TestClient) -> None:
    response = client.post(
        f"{API_PREFIX}/tickets",
        json={
            "title": "Impressora sem toner",
            # "description" is missing
            "category_id": 999,  # Assuming this category does not exist
            "priority": "invalid_priority",  # Invalid priority value
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


def test_list_tickets_returns_invalid_sort_field(client: TestClient) -> None:
    response = client.get(
        f"{API_PREFIX}/tickets",
        params={"sort_field": "invalid_field", "sort_direction": "asc"},
    )
    body = response.json()

    assert response.status_code == 422
    assert body["success"] is False
    assert body["message"] == "Request validation failed."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    errors = body["details"]["errors"]
    assert len(errors) == 1

    error = errors[0]
    assert error["code"] == "enum"
    assert error["field"] == "query -> sort_field"
    assert error["message"] == (
        "Invalid value 'invalid_field'. "
        "Input should be 'id', 'title', 'priority' or 'status'"
    )


def test_list_tickets_returns_invalid_sort_direction(client: TestClient) -> None:
    response = client.get(
        f"{API_PREFIX}/tickets",
        params={"sort_field": "priority", "sort_direction": "invalid_order"},
    )
    body = response.json()

    assert response.status_code == 422
    assert body["success"] is False
    assert body["message"] == "Request validation failed."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    errors = body["details"]["errors"]
    assert len(errors) == 1

    error = errors[0]
    assert error["code"] == "enum"
    assert error["field"] == "query -> sort_direction"
    assert error["message"] == (
        "Invalid value 'invalid_order'. Input should be 'asc' or 'desc'"
    )


def test_list_tickets_filters_by_status(client: TestClient) -> None:
    category_id = _create_category(client)
    open_ticket_id = _create_ticket(
        client,
        title="Monitor sem imagem",
        category_id=category_id,
        priority="low",
    )
    closed_ticket_id = _create_ticket(
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
    category_id = _create_category(client)
    _create_ticket(
        client,
        title="Teclado com falha",
        category_id=category_id,
        priority="low",
    )
    high_priority_ticket_id = _create_ticket(
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
    hardware_category_id = _create_category(client)
    software_category_id = _create_category(
        client, "Software", "Categoria para sistemas", True
    )

    _create_ticket(
        client,
        title="Mouse quebrado",
        category_id=hardware_category_id,
        priority="high",
    )
    expected_ticket_id = _create_ticket(
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
    hardware_category_id = _create_category(client)
    software_category_id = _create_category(
        client, "Software", "Categoria para sistemas", True
    )

    _create_ticket(
        client,
        title="Mouse quebrado",
        category_id=hardware_category_id,
        priority="high",
    )
    expected_ticket_id = _create_ticket(
        client,
        title="ERP lento",
        category_id=software_category_id,
        priority="high",
    )
    _create_ticket(
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


def test_list_tickets_ordered_by_id_descending(client: TestClient) -> None:
    hardware_category_id = _create_category(client)
    software_category_id = _create_category(
        client, "Software", "Categoria para sistemas", True
    )

    _create_ticket(
        client,
        title="Mouse quebrado",
        category_id=hardware_category_id,
        priority="high",
    )
    _create_ticket(
        client,
        title="ERP lento",
        category_id=software_category_id,
        priority="high",
    )
    third_ticket_id = _create_ticket(
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
    hardware_category_id = _create_category(client)
    software_category_id = _create_category(
        client, "Software", "Categoria para sistemas", True
    )

    _create_ticket(
        client,
        title="Mouse quebrado",
        category_id=hardware_category_id,
        priority="high",
    )
    _create_ticket(
        client,
        title="ERP lento",
        category_id=software_category_id,
        priority="medium",
    )
    last_expected_ticket_id = _create_ticket(
        client,
        title="Editor travando",
        category_id=software_category_id,
        priority="low",
    )
    first_expected_ticket_id = _create_ticket(
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
