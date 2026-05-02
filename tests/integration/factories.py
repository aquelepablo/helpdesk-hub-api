from fastapi.testclient import TestClient

from app.main import API_PREFIX


def create_category(
    client: TestClient,
    name: str = "Hardware",
    description: str = "Categoria para testes",
    is_active: bool = True,
) -> int:
    response = client.post(
        f"{API_PREFIX}/categories",
        json={
            "name": name,
            "description": description,
            "is_active": is_active,
        },
    )

    assert response.status_code == 201, {
        "status_code": response.status_code,
        "body": response.json(),
    }

    body = response.json()
    return int(body["data"]["id"])


def create_ticket(
    client: TestClient,
    title: str = "Notebook sem acesso",
    category_id: int | None = None,
    priority: str = "high",
) -> int:
    if category_id is None:
        category_id = create_category(client)

    response = client.post(
        f"{API_PREFIX}/tickets",
        json={
            "title": title,
            "description": "Ticket criado para teste de filtro",
            "category_id": category_id,
            "priority": priority,
        },
    )

    assert response.status_code == 201, {
        "status_code": response.status_code,
        "body": response.json(),
    }

    body = response.json()
    return int(body["data"]["id"])
