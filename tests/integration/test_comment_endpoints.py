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

    assert response.status_code == 201, {
        "status_code": response.status_code,
        "body": response.json(),
    }

    body = response.json()
    return int(body["data"]["id"])


def _create_ticket() -> int:
    category_id = _create_category()

    response = client.post(
        f"{API_PREFIX}/ticket",
        json={
            "title": "Notebook sem acesso",
            "description": "Usuário nao consegue entrar no equipamento",
            "category_id": category_id,
            "priority": "high",
        },
    )

    assert response.status_code == 201, {
        "status_code": response.status_code,
        "body": response.json(),
    }

    body = response.json()
    return int(body["data"]["id"])


def test_list_comments_returns_empty_list_when_ticket_has_no_comments() -> None:
    ticket_id = _create_ticket()

    response = client.get(f"{API_PREFIX}/ticket/{ticket_id}/comment")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Listagem de comentários realizada com sucesso",
        "data": [],
    }


def test_create_comment_returns_created_comment() -> None:
    ticket_id = _create_ticket()

    payload: dict[str, str] = {
        "content": "Primeiro comentário do ticket",
    }

    response = client.post(f"{API_PREFIX}/ticket/{ticket_id}/comment", json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body["success"] is True
    assert body["message"] == "Comentário criado com sucesso"
    assert body["data"]["id"] == 1
    assert body["data"]["ticket_id"] == ticket_id
    assert body["data"]["content"] == "Primeiro comentário do ticket"


def test_list_comments_returns_ticket_comments() -> None:
    ticket_id = _create_ticket()

    client.post(
        f"{API_PREFIX}/ticket/{ticket_id}/comment",
        json={"content": "Primeiro comentário"},
    )
    client.post(
        f"{API_PREFIX}/ticket/{ticket_id}/comment",
        json={"content": "Segundo comentário"},
    )

    response = client.get(f"{API_PREFIX}/ticket/{ticket_id}/comment")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Listagem de comentários realizada com sucesso"
    assert len(body["data"]) == 2
    assert body["data"][0]["content"] == "Primeiro comentário"
    assert body["data"][1]["content"] == "Segundo comentário"


def test_update_comment_returns_updated_comment() -> None:
    ticket_id = _create_ticket()

    created = client.post(
        f"{API_PREFIX}/ticket/{ticket_id}/comment",
        json={"content": "Comentario original"},
    ).json()

    comment_id = created["data"]["id"]

    response = client.patch(
        f"{API_PREFIX}/ticket/{ticket_id}/comment/{comment_id}",
        json={"content": "Comentário atualizado"},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Comentário atualizado com sucesso"
    assert body["data"]["id"] == comment_id
    assert body["data"]["ticket_id"] == ticket_id
    assert body["data"]["content"] == "Comentário atualizado"


@pytest.mark.skip(reason="Definir contrato padronizado para erros de validação.")
def test_create_comment_returns_422_for_invalid_payload() -> None:
    pass


@pytest.mark.skip(reason="Definir comportamento para ticket inexistente.")
def test_list_comments_returns_not_found_for_unknown_ticket() -> None:
    pass


@pytest.mark.skip(reason="Definir comportamento para comentário inexistente.")
def test_update_comment_returns_not_found_for_unknown_comment() -> None:
    pass
