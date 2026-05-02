from app.application.interfaces.repositories.category_repository import (
    ICategoryRepository,
)
from app.domain.entities.category import Category


class ListCategoriesUseCase:
    def __init__(self, category_repository: ICategoryRepository) -> None:
        self._category_repository = category_repository

    def execute(self) -> list[Category]:

        categories = self._category_repository.list_all()

        return categories
