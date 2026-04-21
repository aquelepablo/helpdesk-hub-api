from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository


class ListCategoriesUseCase:
    def __init__(self, repository: CategoryRepository) -> None:
        self.category_repository = repository

    def execute(self) -> list[Category]:

        categories = self.category_repository.list_all()

        return categories
