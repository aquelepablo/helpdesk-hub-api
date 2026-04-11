# CategoryCreateRequest
# CategoryUpdateRequest
# CategoryResponse

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class CategoryCreateRequest(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=100, description="Short category name."
    )
    description: str = Field(
        default="", max_length=500, description="Optional category description."
    )
    is_active: bool = Field(..., description="Indicates if the category is active.")

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Category name cannot be empty or blank.")
        return cleaned_value

    @field_validator("description")
    @classmethod
    def validate_optional_description(cls, value: str) -> str:
        return value.strip()


class CategoryUpdateRequest(BaseModel):
    id: int = Field(..., description="The ID of the category to update.")
    name: str | None = Field(
        default=None, min_length=1, max_length=100, description="Short category name."
    )
    description: str | None = Field(
        default=None,
        min_length=0,
        max_length=500,
        description="Optional category description.",
    )
    is_active: bool | None = Field(
        default=None, description="Indicates if the category is active."
    )

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Category ID must be a positive integer.")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "CategoryUpdateRequest":
        if all(
            value is None for value in (self.name, self.description, self.is_active)
        ):
            raise ValueError("At least one field must be provided for update.")
        return self


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
