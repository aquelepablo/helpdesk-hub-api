from app.application.use_cases.category.repositories.category_repository import (
    CategoryRepository,
)
from app.domain.entities.category import Category


class ListCategoriesUseCase:
    def __init__(self, repository: CategoryRepository) -> None:
        self._category_repository = repository

    def execute(self) -> list[Category]:

        categories = self._category_repository.list_all()

        return categories
