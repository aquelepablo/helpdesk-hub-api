import copy
from datetime import datetime

from app.domain.entities.category import Category
from app.domain.exceptions.category_exceptions import CategoryNotFoundError
from app.infra.db.repositories.memory_database import category_db


class InMemoryCategoryRepository:
    def _find_stored_category_by_id(self, category_id: int) -> Category:
        for category in category_db.categories:
            if category.id == category_id:
                return category

        raise CategoryNotFoundError(category_id)

    def _create(self, category: Category) -> Category:
        category_db.id_counter += 1
        category.id = category_db.id_counter

        category.created_at = datetime.now()
        category.updated_at = datetime.now()

        stored_category = category_db.add(category)

        return stored_category

    def _update(self, category_id: int, updated_category: Category) -> Category:
        stored_category = self._find_stored_category_by_id(category_id)

        stored_category.name = updated_category.name
        stored_category.description = updated_category.description
        stored_category.is_active = updated_category.is_active
        stored_category.updated_at = datetime.now()

        return copy.deepcopy(stored_category)

    def save(self, category: Category) -> Category:
        if category.id is None:
            return self._create(category)
        else:
            return self._update(category.id, category)

    def list_all(self) -> list[Category]:
        return copy.deepcopy(category_db.categories)

    def get_by_id(self, category_id: int) -> Category:
        stored_category = self._find_stored_category_by_id(category_id)
        return copy.deepcopy(stored_category)
