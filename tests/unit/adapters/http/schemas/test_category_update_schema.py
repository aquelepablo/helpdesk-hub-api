import pytest
from pydantic import ValidationError

from app.adapters.http.schemas.category_schema import CategoryUpdateRequest


def test_update_category_schema_requires_at_least_one_field() -> None:
    with pytest.raises(ValidationError):
        CategoryUpdateRequest(id=1)


def test_update_category_schema_rejects_non_positive_id() -> None:
    with pytest.raises(ValidationError):
        CategoryUpdateRequest(id=0, name="Category with invalid ID")
