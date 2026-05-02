from fastapi.testclient import TestClient

from app.main import API_PREFIX


def test_update_category_returns_updated_category(client: TestClient) -> None:
    created = client.post(
        f"{API_PREFIX}/categories",
        json={
            "name": "Software",
            "description": "Falhas em sistemas internos",
            "is_active": True,
        },
    ).json()

    category_id = created["data"]["id"]

    response = client.patch(
        f"{API_PREFIX}/categories/{category_id}",
        json={
            "name": "Software Corporativo",
            "is_active": False,
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["id"] == category_id
    assert body["message"] == "Categoria atualizada com sucesso"
    assert body["data"]["name"] == "Software Corporativo"
    assert body["data"]["is_active"] is False


def test_update_category_returns_not_found_for_unknown_id(client: TestClient) -> None:
    invalid_category_id = 999

    response = client.patch(
        f"{API_PREFIX}/categories/{invalid_category_id}",
        json={
            "name": "Acesso",
            "description": "Permissões e credenciais",
            "is_active": True,
        },
    )
    body = response.json()
    assert response.status_code == 404
    assert body["success"] is False
    assert body["message"] == f"Category with id {invalid_category_id} was not found."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    error_codes = {error["code"] for error in body["details"]["errors"]}

    assert "not_found" in error_codes
