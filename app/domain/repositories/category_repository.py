from abc import ABC, abstractmethod

from app.domain.entities.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def create(self, category: Category) -> Category:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: int) -> Category:
        raise NotImplementedError

    @abstractmethod
    def update(self, updated_category: Category) -> Category:
        raise NotImplementedError
