from fastapi.testclient import TestClient

from app.main import API_PREFIX


def test_create_category_returns_created_category(client: TestClient) -> None:
    payload: dict[str, str | bool] = {
        "name": "Hardware",
        "description": "Problemas físicos com equipamentos",
        "is_active": True,
    }

    response = client.post(f"{API_PREFIX}/categories", json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body["success"] is True
    assert body["message"] == "Categoria criada com sucesso"
    assert body["data"]["id"] == 1
    assert body["data"]["name"] == "Hardware"
    assert body["data"]["description"] == "Problemas físicos com equipamentos"
    assert body["data"]["is_active"] is True


def test_create_category_returns_422_for_invalid_payload(client: TestClient) -> None:
    response = client.post(
        f"{API_PREFIX}/categories",
        json={
            "is_active": True,
        },
    )
    body = response.json()

    assert response.status_code == 422
    assert body["success"] is False
    assert body["message"] == "Request validation failed."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    error_fields = {error["field"] for error in body["details"]["errors"]}

    assert "name" in error_fields
