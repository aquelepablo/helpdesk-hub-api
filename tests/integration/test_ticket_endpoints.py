import pytest
from fastapi.testclient import TestClient

from app.infra.db.repositories.memory_database import ticket_db
from app.main import API_PREFIX, app

client = TestClient(app)


def _reset_ticket_memory() -> None:
    ticket_db.id_counter = 0
    ticket_db.tickets.clear()


def test_list_tickets_returns_empty_list_when_memory_is_empty() -> None:
    _reset_ticket_memory()

    response = client.get(f"{API_PREFIX}/ticket")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Listagem de tickets realizada com sucesso",
        "data": [],
    }


def test_create_ticket_returns_created_ticket() -> None:
    _reset_ticket_memory()

    payload: dict[str, str | int] = {
        "title": "Notebook sem acesso",
        "description": "Usuário nao consegue entrar no equipamento",
        "category_id": 1,
        "priority": "high",
        "status": "open",
    }

    response = client.post(f"{API_PREFIX}/ticket", json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body["success"] is True
    assert body["message"] == "Ticket criado com sucesso"
    assert body["data"]["id"] == 1
    assert body["data"]["title"] == "Notebook sem acesso"
    assert body["data"]["category_id"] == 1
    assert body["data"]["priority"] == "high"
    assert body["data"]["status"] == "open"


def test_get_ticket_by_id_returns_ticket_details() -> None:
    _reset_ticket_memory()

    created = client.post(
        f"{API_PREFIX}/ticket",
        json={
            "title": "Email bloqueado",
            "description": "Nao recebe mensagens externas",
            "category_id": 2,
            "priority": "medium",
            "status": "open",
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
    _reset_ticket_memory()

    created = client.post(
        f"{API_PREFIX}/ticket",
        json={
            "title": "VPN instável",
            "description": "Conexão cai durante o expediente",
            "category_id": 3,
            "priority": "low",
            "status": "open",
        },
    ).json()

    response = client.patch(
        f"{API_PREFIX}/ticket",
        json={
            "id": created["data"]["id"],
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
