from app.application.use_cases.category.repositories.category_repository import (
    CategoryRepository,
)
from app.domain.entities.category import Category


class GetCategoryByIdUseCase:
    def __init__(self, repository: CategoryRepository) -> None:
        self._category_repository = repository

    def execute(self, category_id: int) -> Category:

        category = self._category_repository.get_by_id(category_id)

        return category
