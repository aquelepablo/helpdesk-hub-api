import pytest
from fastapi.testclient import TestClient

from app.main import API_PREFIX, app

client = TestClient(app)


def _create_category() -> int:
    response = client.post(
        f"{API_PREFIX}/category",
        json={
            "name": "Hardware",
            "description": "Categoria para testes",
            "is_active": True,
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
        f"{API_PREFIX}/ticket",
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
    response = client.get(f"{API_PREFIX}/ticket")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Listagem de tickets realizada com sucesso",
        "data": [],
    }


def test_create_ticket_returns_created_ticket() -> None:
    category_id = _create_category()

    payload: dict[str, str | int] = {
        "title": "Notebook sem acesso",
        "description": "Usuário nao consegue entrar no equipamento",
        "category_id": category_id,
        "priority": "high",
    }

    response = client.post(f"{API_PREFIX}/ticket", json=payload)
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
        f"{API_PREFIX}/ticket",
        json={
            "title": "Email bloqueado",
            "description": "Nao recebe mensagens externas",
            "category_id": category_id,
            "priority": "medium",
        },
    ).json()

    ticket_id = created["data"]["id"]

    response = client.get(f"{API_PREFIX}/ticket/{ticket_id}")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["id"] == ticket_id
    assert body["data"]["title"] == "Email bloqueado"


def test_update_ticket_returns_updated_ticket() -> None:
    category_id = _create_category()

    created = client.post(
        f"{API_PREFIX}/ticket",
        json={
            "title": "VPN instável",
            "description": "Conexão cai durante o expediente",
            "category_id": category_id,
            "priority": "low",
        },
    ).json()

    ticket_id = created["data"]["id"]

    response = client.patch(
        f"{API_PREFIX}/ticket/{ticket_id}",
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


@pytest.mark.skip(reason="Definir contrato padronizado para erros de validação.")
def test_create_ticket_returns_422_for_invalid_payload() -> None:
    pass


@pytest.mark.skip(reason="Definir comportamento para ticket inexistente.")
def test_get_ticket_by_id_returns_not_found_for_unknown_id() -> None:
    pass


@pytest.mark.skip(reason="Definir comportamento para update de ticket inexistente.")
def test_update_ticket_returns_not_found_for_unknown_id() -> None:
    pass


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
        f"{API_PREFIX}/ticket/{closed_ticket_id}",
        json={"status": "closed"},
    )

    response = client.get(f"{API_PREFIX}/ticket", params={"status": "open"})
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == open_ticket_id
    assert body["data"][0]["status"] == "open"


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

    response = client.get(f"{API_PREFIX}/ticket", params={"priority": "high"})
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == high_priority_ticket_id
    assert body["data"][0]["priority"] == "high"


def test_list_tickets_filters_by_category() -> None:
    hardware_category_id = _create_category()
    software_category = client.post(
        f"{API_PREFIX}/category",
        json={
            "name": "Software",
            "description": "Categoria para sistemas",
            "is_active": True,
        },
    ).json()
    software_category_id = software_category["data"]["id"]

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
        f"{API_PREFIX}/ticket", params={"category_id": software_category_id}
    )
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == expected_ticket_id
    assert body["data"][0]["priority"] == "high"


def test_list_tickets_filters_by_category_and_priority() -> None:
    hardware_category_id = _create_category()
    software_category = client.post(
        f"{API_PREFIX}/category",
        json={
            "name": "Software",
            "description": "Categoria para sistemas",
            "is_active": True,
        },
    ).json()
    software_category_id = software_category["data"]["id"]

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
        f"{API_PREFIX}/ticket",
        params={
            "category_id": software_category_id,
            "priority": "high",
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert len(body["data"]) == 1
    assert body["data"][0]["id"] == expected_ticket_id
    assert body["data"][0]["category_id"] == software_category_id
    assert body["data"][0]["priority"] == "high"
