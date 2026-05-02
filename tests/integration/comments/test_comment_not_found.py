from fastapi.testclient import TestClient

from app.main import API_PREFIX
from tests.integration.factories import create_ticket


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
    ticket_id = create_ticket(client)
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
