from fastapi.testclient import TestClient

from app.main import API_PREFIX
from tests.integration.factories import create_ticket


def test_update_comment_returns_updated_comment(client: TestClient) -> None:
    ticket_id = create_ticket(client)

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
