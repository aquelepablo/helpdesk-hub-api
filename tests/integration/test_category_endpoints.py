from fastapi.testclient import TestClient

from app.application.bootstrap.default_categories import DEFAULT_CATEGORIES
from app.infrastructure.bootstrap.seed_categories import seed_categories
from app.main import API_PREFIX


def test_list_categories_returns_empty_list_when_memory_is_empty(
    client: TestClient,
) -> None:
    response = client.get(f"{API_PREFIX}/categories")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Categorias listadas com sucesso"
    assert body["data"] == []


def test_create_category_returns_created_category(client: TestClient) -> None:
    payload: dict[str, str | bool] = {
        "name": "Hardware",
        "description": "Problemas fÍsicos com equipamentos",
        "is_active": True,
    }

    response = client.post(f"{API_PREFIX}/categories", json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body["success"] is True
    assert body["message"] == "Categoria criada com sucesso"
    assert body["data"]["id"] == 1
    assert body["data"]["name"] == "Hardware"
    assert body["data"]["description"] == "Problemas fÍsicos com equipamentos"
    assert body["data"]["is_active"] is True


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


def test_create_category_returns_422_for_invalid_payload(client: TestClient) -> None:
    response = client.post(
        f"{API_PREFIX}/categories",
        json={
            # name is missing
            # description is missing
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


def test_create_categories_with_bootstrap(client: TestClient) -> None:
    seed_categories()

    response = client.get(f"{API_PREFIX}/categories")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Categorias listadas com sucesso"

    assert len(body["data"]) == len(DEFAULT_CATEGORIES)

    categories_by_name = {category["name"]: category for category in body["data"]}

    for expected_category in DEFAULT_CATEGORIES:
        category = categories_by_name[expected_category["name"]]

        assert category["description"] == expected_category["description"]
        assert category["is_active"] == expected_category["is_active"]


def test_create_categories_with_bootstrap_is_idempotent(client: TestClient) -> None:
    seed_categories()
    seed_categories()

    response = client.get(f"{API_PREFIX}/categories")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Categorias listadas com sucesso"

    assert len(body["data"]) == len(DEFAULT_CATEGORIES)
