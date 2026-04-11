from dataclasses import dataclass

from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository


@dataclass(slots=True)
class UpdateCategoryInput:
    category_id: int
    name: str | None
    description: str | None
    is_active: bool | None


class UpdateCategoryUseCase:
    def __init__(self, repository: CategoryRepository) -> None:
        self._category_repository = repository

    def execute(self, input_data: UpdateCategoryInput) -> Category:

        existing_category = self._category_repository.get_by_id(input_data.category_id)

        if input_data.name is not None:
            existing_category.name = input_data.name

        if input_data.description is not None:
            existing_category.description = input_data.description

        if input_data.is_active is not None:
            existing_category.is_active = input_data.is_active

        return self._category_repository.update(existing_category)
