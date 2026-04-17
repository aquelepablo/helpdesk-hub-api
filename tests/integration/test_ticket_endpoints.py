import pytest
from fastapi.testclient import TestClient

from app.infra.db.repositories.memory_database import category_db, ticket_db
from app.main import API_PREFIX, app

client = TestClient(app)


def _reset_ticket_memory() -> None:
    ticket_db.id_counter = 0
    ticket_db.tickets.clear()


def _reset_category_memory() -> None:
    category_db.id_counter = 0
    category_db.categories.clear()


@pytest.fixture(autouse=True)
def reset_memory() -> None:
    _reset_category_memory()
    _reset_ticket_memory()


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
