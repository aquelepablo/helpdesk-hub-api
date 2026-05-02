from fastapi.testclient import TestClient

from app.main import API_PREFIX


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
