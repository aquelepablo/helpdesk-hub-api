import pytest
from pydantic import ValidationError

from app.adapters.http.schemas.category_schema import CategoryUpdateRequest


def test_update_category_schema_requires_at_least_one_field() -> None:
    with pytest.raises(ValidationError):
        CategoryUpdateRequest()


def test_update_category_schema_accepts_only_name() -> None:
    schema = CategoryUpdateRequest(name="Update only Category Name")

    assert schema.name == "Update only Category Name"
    assert schema.description is None
    assert schema.is_active is None


def test_update_category_schema_accepts_only_description() -> None:
    schema = CategoryUpdateRequest(description="Update only Category Description")

    assert schema.name is None
    assert schema.description == "Update only Category Description"
    assert schema.is_active is None


def test_update_category_schema_accepts_empty_description() -> None:
    schema = CategoryUpdateRequest(description=" ")

    assert schema.name is None
    assert schema.description == ""
    assert schema.is_active is None


def test_update_category_schema_accepts_only_is_active() -> None:
    schema = CategoryUpdateRequest(is_active=False)

    assert schema.name is None
    assert schema.description is None
    assert schema.is_active is False


def test_update_category_schema_rejects_blank_name() -> None:
    with pytest.raises(ValidationError):
        CategoryUpdateRequest(name=" ")


def test_update_category_schema_rejects_extra_fields() -> None:
    payload: dict[str, object] = {
        "name": "Updated category",
        "priority": "high",
    }

    with pytest.raises(ValidationError):
        CategoryUpdateRequest.model_validate(payload)


def test_update_category_schema_rejects_id_in_body() -> None:
    payload: dict[str, object] = {
        "id": 1,
        "name": "Updated category",
    }

    with pytest.raises(ValidationError):
        CategoryUpdateRequest.model_validate(payload)
