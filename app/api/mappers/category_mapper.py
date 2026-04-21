from app.api.schemas.category_schema import (
    CategoryCreateRequest,
    CategoryUpdateRequest,
)
from app.application.use_cases.category.create_category import CreateCategoryInput
from app.application.use_cases.category.update_category import UpdateCategoryInput


def to_create_category_input(request: CategoryCreateRequest) -> CreateCategoryInput:
    return CreateCategoryInput(
        name=request.name,
        description=request.description,
        is_active=request.is_active,
    )


def to_update_category_input(request: CategoryUpdateRequest) -> UpdateCategoryInput:
    return UpdateCategoryInput(
        name=request.name,
        description=request.description,
        is_active=request.is_active,
    )
