from app.domain.entities.category import Category
from app.domain.repositories.category_repository import CategoryRepository


class GetCategoryByIdUseCase:
    def __init__(self, repository: CategoryRepository) -> None:
        self.category_repository = repository

    def execute(self, category_id: int) -> Category:

        category = self.category_repository.get_by_id(category_id)

        return category
