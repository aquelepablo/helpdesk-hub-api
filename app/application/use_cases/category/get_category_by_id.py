from app.application.ports.category_repository import (
    CategoryRepository,
)
from app.domain.entities.category import Category


class GetCategoryByIdUseCase:
    def __init__(self, category_repository: CategoryRepository) -> None:
        self._category_repository = category_repository

    def execute(self, category_id: int) -> Category:

        category = self._category_repository.get_by_id(category_id)

        return category
