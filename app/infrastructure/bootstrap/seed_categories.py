from app.application.bootstrap.default_categories import DEFAULT_CATEGORIES
from app.domain.entities.category import Category
from app.infrastructure.db.repositories.sqlalchemy.category_repository import (
    SQLAlchemyCategoryRepository,
)
from app.infrastructure.db.sqlalchemy.database import get_db_session


def seed_categories() -> None:
    session_generator = get_db_session()

    try:
        session = next(session_generator)
        category_repository = SQLAlchemyCategoryRepository(session)
        existing_categories = category_repository.list_all()
        existing_category_names = {category.name for category in existing_categories}

        for category_data in DEFAULT_CATEGORIES:
            if category_data["name"] not in existing_category_names:
                category = Category(
                    name=category_data["name"],
                    description=category_data["description"],
                    is_active=category_data["is_active"],
                )
                category_repository.create(category)

    finally:
        session_generator.close()
