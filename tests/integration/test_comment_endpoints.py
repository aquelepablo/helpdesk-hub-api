from fastapi.testclient import TestClient

from app.main import API_PREFIX


def _create_category(client: TestClient) -> int:
    response = client.post(
        f"{API_PREFIX}/categories",
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


def _create_ticket(client: TestClient) -> int:
    category_id = _create_category(client)

    response = client.post(
        f"{API_PREFIX}/tickets",
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


def test_list_comments_returns_empty_list_when_ticket_has_no_comments(
    client: TestClient,
) -> None:
    ticket_id = _create_ticket(client)

    response = client.get(f"{API_PREFIX}/tickets/{ticket_id}/comments")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Comentários listados com sucesso",
        "data": [],
    }


def test_create_comment_returns_created_comment(client: TestClient) -> None:
    ticket_id = _create_ticket(client)

    payload: dict[str, str] = {
        "content": "Primeiro comentário do ticket",
    }

    response = client.post(f"{API_PREFIX}/tickets/{ticket_id}/comments", json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body["success"] is True
    assert body["message"] == "Comentário criado com sucesso"
    assert body["data"]["id"] == 1
    assert body["data"]["ticket_id"] == ticket_id
    assert body["data"]["content"] == "Primeiro comentário do ticket"


def test_list_comments_returns_ticket_comments(client: TestClient) -> None:
    ticket_id = _create_ticket(client)

    client.post(
        f"{API_PREFIX}/tickets/{ticket_id}/comments",
        json={"content": "Primeiro comentário"},
    )
    client.post(
        f"{API_PREFIX}/tickets/{ticket_id}/comments",
        json={"content": "Segundo comentário"},
    )

    response = client.get(f"{API_PREFIX}/tickets/{ticket_id}/comments")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Comentários listados com sucesso"
    assert len(body["data"]) == 2
    assert body["data"][0]["content"] == "Primeiro comentário"
    assert body["data"][1]["content"] == "Segundo comentário"


def test_update_comment_returns_updated_comment(client: TestClient) -> None:
    ticket_id = _create_ticket(client)

    created = client.post(
        f"{API_PREFIX}/tickets/{ticket_id}/comments",
        json={"content": "Comentário original"},
    ).json()

    comment_id = created["data"]["id"]

    response = client.patch(
        f"{API_PREFIX}/tickets/{ticket_id}/comments/{comment_id}",
        json={"content": "Comentário atualizado"},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Comentário atualizado com sucesso"
    assert body["data"]["id"] == comment_id
    assert body["data"]["ticket_id"] == ticket_id
    assert body["data"]["content"] == "Comentário atualizado"


def test_create_comment_returns_422_for_invalid_empty_comment(
    client: TestClient,
) -> None:
    ticket_id = 1
    response = client.post(
        f"{API_PREFIX}/tickets/{ticket_id}/comments",
        json={"content": "   "},
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
    assert error["code"] == "value_error"
    assert error["field"] == "content"
    assert error["message"] == "Value error, Comment cannot be empty or blank."


def test_create_comment_returns_422_for_invalid_payload(client: TestClient) -> None:
    ticket_id = 1
    response = client.post(
        f"{API_PREFIX}/tickets/{ticket_id}/comments",
        json={"content": "Comentário", "invalid_field": ""},
    )
    body = response.json()

    assert response.status_code == 422
    assert body["success"] is False
    assert body["message"] == "Request validation failed."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    error_fields = {error["field"] for error in body["details"]["errors"]}

    assert "invalid_field" in error_fields


def test_list_comments_returns_not_found_for_unknown_ticket(client: TestClient) -> None:
    invalid_ticket_id = 999

    response = client.get(f"{API_PREFIX}/tickets/{invalid_ticket_id}/comments")
    body = response.json()

    assert response.status_code == 404
    assert body["success"] is False
    assert body["message"] == f"Ticket with id {invalid_ticket_id} was not found."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    error_codes = {error["code"] for error in body["details"]["errors"]}

    assert "not_found" in error_codes


def test_update_comment_returns_not_found_for_unknown_comment(
    client: TestClient,
) -> None:
    ticket_id = _create_ticket(client)
    invalid_comment_id = 999

    response = client.patch(
        f"{API_PREFIX}/tickets/{ticket_id}/comments/{invalid_comment_id}",
        json={"content": "Comentário atualizado"},
    )
    body = response.json()

    assert response.status_code == 404
    assert body["success"] is False
    assert body["message"] == f"Comment with id {invalid_comment_id} was not found."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    error_codes = {error["code"] for error in body["details"]["errors"]}

    assert "not_found" in error_codes
