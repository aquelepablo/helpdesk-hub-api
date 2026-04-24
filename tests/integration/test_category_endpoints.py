from fastapi.testclient import TestClient

from app.main import API_PREFIX, app

client = TestClient(app)


def test_list_categories_returns_empty_list_when_memory_is_empty() -> None:
    response = client.get(f"{API_PREFIX}/category")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Listagem de categorias realizada com sucesso",
        "data": [],
    }


def test_create_category_returns_created_category() -> None:
    payload: dict[str, str | bool] = {
        "name": "Hardware",
        "description": "Problemas fÍsicos com equipamentos",
        "is_active": True,
    }

    response = client.post(f"{API_PREFIX}/category", json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body["success"] is True
    assert body["message"] == "Categoria criada com sucesso"
    assert body["data"]["id"] == 1
    assert body["data"]["name"] == "Hardware"
    assert body["data"]["description"] == "Problemas fÍsicos com equipamentos"
    assert body["data"]["is_active"] is True


def test_get_category_by_id_returns_category_details() -> None:
    created = client.post(
        f"{API_PREFIX}/category",
        json={
            "name": "Acesso",
            "description": "Permissões e credenciais",
            "is_active": True,
        },
    ).json()

    category_id = created["data"]["id"]

    response = client.get(f"{API_PREFIX}/category/{category_id}")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["message"] == "Detalhes da categoria obtidos com sucesso"
    assert body["data"]["id"] == category_id
    assert body["data"]["name"] == "Acesso"


def test_update_category_returns_updated_category() -> None:
    created = client.post(
        f"{API_PREFIX}/category",
        json={
            "name": "Software",
            "description": "Falhas em sistemas internos",
            "is_active": True,
        },
    ).json()

    category_id = created["data"]["id"]

    response = client.patch(
        f"{API_PREFIX}/category/{category_id}",
        json={
            "name": "Software Corporativo",
            "is_active": False,
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["id"] == 1
    assert body["message"] == "Categoria atualizada com sucesso"
    assert body["data"]["name"] == "Software Corporativo"
    assert body["data"]["is_active"] is False


def test_create_category_returns_422_for_invalid_payload() -> None:
    response = client.post(
        f"{API_PREFIX}/category",
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


def test_get_category_by_id_returns_not_found_for_unknown_id() -> None:
    invalid_category_id = 999

    response = client.get(f"{API_PREFIX}/category/{invalid_category_id}")
    body = response.json()

    assert response.status_code == 404
    assert body["success"] is False
    assert body["message"] == f"Category with id {invalid_category_id} was not found."
    assert "details" in body
    assert "errors" in body["details"]
    assert len(body["details"]["errors"]) >= 1

    error_codes = {error["code"] for error in body["details"]["errors"]}

    assert "not_found" in error_codes


def test_update_category_returns_not_found_for_unknown_id() -> None:
    invalid_category_id = 999

    response = client.patch(
        f"{API_PREFIX}/category/{invalid_category_id}",
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
