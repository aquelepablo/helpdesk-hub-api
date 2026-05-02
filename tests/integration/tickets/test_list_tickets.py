from fastapi.testclient import TestClient

from app.main import API_PREFIX


def test_list_tickets_returns_empty_list_when_memory_is_empty(
    client: TestClient,
) -> None:
    response = client.get(f"{API_PREFIX}/tickets")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Tickets listados com sucesso",
        "items": [],
        "total_items": 0,
        "page": 1,
        "page_size": 10,
        "total_pages": 0,
    }


def test_list_tickets_returns_invalid_sort_field(client: TestClient) -> None:
    response = client.get(
        f"{API_PREFIX}/tickets",
        params={"sort_field": "invalid_field", "sort_direction": "asc"},
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
    assert error["code"] == "enum"
    assert error["field"] == "query -> sort_field"
    assert error["message"] == (
        "Invalid value 'invalid_field'. "
        "Input should be 'id', 'title', 'priority' or 'status'"
    )


def test_list_tickets_returns_invalid_sort_direction(client: TestClient) -> None:
    response = client.get(
        f"{API_PREFIX}/tickets",
        params={"sort_field": "priority", "sort_direction": "invalid_order"},
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
    assert error["code"] == "enum"
    assert error["field"] == "query -> sort_direction"
    assert error["message"] == (
        "Invalid value 'invalid_order'. Input should be 'asc' or 'desc'"
    )
