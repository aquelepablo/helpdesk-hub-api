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
