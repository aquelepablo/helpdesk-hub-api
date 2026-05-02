from fastapi.testclient import TestClient

from app.main import API_PREFIX
from tests.integration.factories import create_ticket


def test_create_comment_returns_created_comment(client: TestClient) -> None:
    ticket_id = create_ticket(client)

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
