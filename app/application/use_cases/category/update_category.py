from dataclasses import dataclass

from app.application.use_cases.category.repositories.category_repository import (
    CategoryRepository,
)
from app.domain.entities.category import Category


@dataclass(slots=True)
class UpdateCategoryInput:
    name: str | None
    description: str | None
    is_active: bool | None


class UpdateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository) -> None:
        self._category_repository = category_repository

    def execute(self, category_id: int, input_data: UpdateCategoryInput) -> Category:

        existing_category = self._category_repository.get_by_id(category_id)

        if input_data.name is not None:
            existing_category.name = input_data.name

        if input_data.description is not None:
            existing_category.description = input_data.description

        if input_data.is_active is not None:
            existing_category.is_active = input_data.is_active

        return self._category_repository.save(existing_category)
