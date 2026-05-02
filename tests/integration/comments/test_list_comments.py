from fastapi.testclient import TestClient

from app.main import API_PREFIX
from tests.integration.factories import create_ticket


def test_list_comments_returns_empty_list_when_ticket_has_no_comments(
    client: TestClient,
) -> None:
    ticket_id = create_ticket(client)

    response = client.get(f"{API_PREFIX}/tickets/{ticket_id}/comments")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Comentários listados com sucesso",
        "data": [],
    }


def test_list_comments_returns_ticket_comments(client: TestClient) -> None:
    ticket_id = create_ticket(client)

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
