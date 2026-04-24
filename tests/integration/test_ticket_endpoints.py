from fastapi.testclient import TestClient

from app.main import API_PREFIX, app

client = TestClient(app)


def _create_category(
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
    *,
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


def test_list_tickets_returns_empty_list_when_memory_is_empty() -> None:
    response = client.get(f"{API_PREFIX}/tickets")

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "total_items": 0,
        "page": 1,
        "page_size": 10,
        "total_pages": 0,
    }


def test_list_tickets_returns_paginated_tickets() -> None:
    category_id = _create_category()

    first_ticket_id = _create_ticket(
        title="Ticket 1",
        category_id=category_id,
        priority="low",
    )
    second_ticket_id = _create_ticket(
        title="Ticket 2",
        category_id=category_id,
        priority="medium",
    )
    third_ticket_id = _create_ticket(
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
    assert body["total_items"] == 3
    assert body["page"] == 2
    assert body["page_size"] == 2
    assert body["total_pages"] == 2
    assert len(body["items"]) == 1
    assert body["items"][0]["id"] == third_ticket_id
    assert body["items"][0]["id"] not in (first_ticket_id, second_ticket_id)


def test_create_ticket_returns_created_ticket() -> None:
    category_id = _create_category()

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


def test_get_ticket_by_id_returns_ticket_details() -> None:
    category_id = _create_category()

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


def test_update_ticket_returns_updated_ticket() -> None:
    category_id = _create_category()

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


def test_create_ticket_returns_422_for_invalid_payload() -> None:
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


def test_get_ticket_by_id_returns_not_found_for_unknown_id() -> None:

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


def test_update_ticket_returns_not_found_for_unknown_id() -> None:
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


def test_list_tickets_filters_by_status() -> None:
    category_id = _create_category()
    open_ticket_id = _create_ticket(
        title="Monitor sem imagem",
        category_id=category_id,
        priority="low",
    )
    closed_ticket_id = _create_ticket(
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


def test_list_tickets_filters_by_priority() -> None:
    category_id = _create_category()
    _create_ticket(
        title="Teclado com falha",
        category_id=category_id,
        priority="low",
    )
    high_priority_ticket_id = _create_ticket(
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


def test_list_tickets_filters_by_category() -> None:
    hardware_category_id = _create_category()
    software_category_id = _create_category("Software", "Categoria para sistemas", True)

    _create_ticket(
        title="Mouse quebrado",
        category_id=hardware_category_id,
        priority="high",
    )
    expected_ticket_id = _create_ticket(
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


def test_list_tickets_filters_by_category_and_priority() -> None:
    hardware_category_id = _create_category()
    software_category_id = _create_category("Software", "Categoria para sistemas", True)

    _create_ticket(
        title="Mouse quebrado",
        category_id=hardware_category_id,
        priority="high",
    )
    expected_ticket_id = _create_ticket(
        title="ERP lento",
        category_id=software_category_id,
        priority="high",
    )
    _create_ticket(
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


def test_list_tickets_ordered_by_id_descending() -> None:
    hardware_category_id = _create_category()
    software_category_id = _create_category("Software", "Categoria para sistemas", True)

    _create_ticket(
        title="Mouse quebrado",
        category_id=hardware_category_id,
        priority="high",
    )
    _create_ticket(
        title="ERP lento",
        category_id=software_category_id,
        priority="high",
    )
    third_ticket_id = _create_ticket(
        title="Editor travando",
        category_id=software_category_id,
        priority="low",
    )

    response = client.get(
        f"{API_PREFIX}/tickets",
        params={"sort_order": "desc"},
    )
    body = response.json()

    assert response.status_code == 200
    assert len(body["items"]) == 3
    assert body["items"][0]["id"] == third_ticket_id
    assert body["items"][0]["category_id"] == software_category_id
    assert body["items"][0]["priority"] == "low"


def test_list_tickets_ordered_by_priority_descending() -> None:
    hardware_category_id = _create_category()
    software_category_id = _create_category("Software", "Categoria para sistemas", True)

    _create_ticket(
        title="Mouse quebrado",
        category_id=hardware_category_id,
        priority="high",
    )
    _create_ticket(
        title="ERP lento",
        category_id=software_category_id,
        priority="medium",
    )
    last_expected_ticket_id = _create_ticket(
        title="Editor travando",
        category_id=software_category_id,
        priority="low",
    )
    first_expected_ticket_id = _create_ticket(
        title="Sistema offline",
        category_id=software_category_id,
        priority="urgent",
    )

    response = client.get(
        f"{API_PREFIX}/tickets",
        params={"sort_field": "priority", "sort_order": "desc"},
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
