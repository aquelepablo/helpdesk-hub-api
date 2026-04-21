from app.application.bootstrap.default_categories import DEFAULT_CATEGORIES
from app.domain.entities.category import Category
from app.infrastructure.db.repositories.category_repository import (
    InMemoryCategoryRepository,
)


def seed_categories() -> None:
    category_repository = InMemoryCategoryRepository()
    existing_categories = category_repository.list_all()
    existing_category_names = {category.name for category in existing_categories}

    for category_data in DEFAULT_CATEGORIES:
        if category_data["name"] not in existing_category_names:
            category = Category(
                name=category_data["name"],
                description=category_data["description"],
                is_active=category_data["is_active"],
            )
            category_repository.save(category)
