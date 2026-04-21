from dataclasses import dataclass

from app.application.interfaces.repositories.category_repository import (
    CategoryRepository,
)
from app.domain.entities.category import Category


@dataclass(slots=True)
class CreateCategoryInput:
    name: str
    description: str
    is_active: bool


class CreateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepository) -> None:
        self._category_repository = category_repository

    def execute(self, input_data: CreateCategoryInput) -> Category:

        new_category = Category(
            name=input_data.name,
            description=input_data.description,
            is_active=input_data.is_active,
        )

        persisted_category = self._category_repository.save(new_category)

        return persisted_category
