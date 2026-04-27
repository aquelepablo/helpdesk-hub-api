from abc import ABC, abstractmethod

from app.domain.entities.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category: ...

    @abstractmethod
    def list_all(self) -> list[Category]: ...

    @abstractmethod
    def get_by_id(self, category_id: int) -> Category: ...
