from dataclasses import dataclass

from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository


@dataclass(slots=True)
class CreateCategoryInput:
    name: str
    description: str
    is_active: bool


class CreateCategoryUseCase:
    def __init__(self, repository: CategoryRepository) -> None:
        self._category_repository = repository

    def execute(self, input_data: CreateCategoryInput) -> Category:

        new_category = Category(
            name=input_data.name,
            description=input_data.description,
            is_active=input_data.is_active,
        )

        persisted_category = self._category_repository.create(new_category)

        return persisted_category
