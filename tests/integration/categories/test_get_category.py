from fastapi.testclient import TestClient

from app.main import API_PREFIX


def test_get_category_by_id_returns_category_details(client: TestClient) -> None:
    created = client.post(
        f"{API_PREFIX}/categories",
        json={
            "name": "Acesso",
            "description": "Permissões e credenciais",
            "is_active": True,
        },
    ).json()

    category_id = created["data"]["id"]

    response = client.get(f"{API_PREFIX}/categories/{category_id}")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Categoria obtida com sucesso"
    assert body["data"]["id"] == category_id
    assert body["data"]["name"] == "Acesso"


def test_get_category_by_id_returns_not_found_for_unknown_id(
    client: TestClient,
) -> None:
    invalid_category_id = 999

    response = client.get(f"{API_PREFIX}/categories/{invalid_category_id}")
    body = response.json()

    assert response.status_code == 404
    assert body["success"] is False
    assert body["message"] == f"Category with id {invalid_category_id} was not found."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    error_codes = {error["code"] for error in body["details"]["errors"]}

    assert "not_found" in error_codes
