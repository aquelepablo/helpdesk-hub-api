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
