import pytest
from pydantic import ValidationError

from app.adapters.http.schemas.category_schema import CategoryCreateRequest


def test_create_category_schema_accepts_valid_data() -> None:
    schema = CategoryCreateRequest(
        name="Test Category",
        description="A category for testing purposes",
        is_active=True,
    )

    assert schema.name == "Test Category"
    assert schema.description == "A category for testing purposes"
    assert schema.is_active is True


def test_create_category_schema_rejects_blank_name() -> None:
    with pytest.raises(ValidationError):
        CategoryCreateRequest(
            name="   ",
            description="A category with blank name",
            is_active=True,
        )


def test_create_category_schema_rejects_extra_fields() -> None:
    payload: dict[str, object] = {
        "name": "Test Category",
        "description": "A category for testing purposes",
        "is_active": True,
        "priority": "high",
    }

    with pytest.raises(ValidationError):
        CategoryCreateRequest.model_validate(payload)


def test_create_category_schema_trims_name_and_description() -> None:
    schema = CategoryCreateRequest(
        name="  Hardware  ",
        description="  Devices and peripherals  ",
        is_active=True,
    )

    assert schema.name == "Hardware"
    assert schema.description == "Devices and peripherals"


def test_create_category_schema_allows_empty_description() -> None:
    schema = CategoryCreateRequest(
        name="Hardware",
        description="   ",
        is_active=True,
    )

    assert schema.description == ""


def test_create_category_schema_rejects_missing_is_active() -> None:
    payload: dict[str, object] = {
        "name": "Hardware",
        "description": "Devices and peripherals",
    }

    with pytest.raises(ValidationError):
        CategoryCreateRequest.model_validate(payload)
