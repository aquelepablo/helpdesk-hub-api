from app.domain.entities.category import Category
from app.domain.exceptions.category_exceptions import CategoryNotFoundError
from app.infrastructure.db.sqlalchemy.models import CategoryORM
from sqlalchemy import select
from sqlalchemy.orm import Session


class SQLAlchemyCategoryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    # ========== Contract methods ==========
    def create(self, category: Category) -> Category:

        if not category:
            raise ValueError("Category cannot be None")

        category_orm = CategoryORM(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

        self._session.add(category_orm)
        self._session.commit()
        self._session.refresh(category_orm)

        return self._orm_to_domain(category_orm)

    def update(self, updated_category: Category) -> Category:

        if not updated_category.id or updated_category.id <= 0:
            raise ValueError("Category must have a valid ID")

        category_orm = self._get_category_orm(updated_category.id)

        category_orm.name = updated_category.name
        category_orm.description = updated_category.description
        category_orm.is_active = updated_category.is_active

        self._session.commit()
        self._session.refresh(category_orm)

        return self._orm_to_domain(category_orm)

    def list_all(self) -> list[Category]:
        categories_orm = self._session.scalars(select(CategoryORM)).all()

        return [self._orm_to_domain(category_orm) for category_orm in categories_orm]

    def get_by_id(self, category_id: int) -> Category:
        category_orm = self._get_category_orm(category_id)

        return self._orm_to_domain(category_orm)

    # ========== Private methods ==========
    def _get_category_orm(self, category_id: int) -> CategoryORM:

        category_orm = self._session.get(CategoryORM, category_id)

        if category_orm is None:
            raise CategoryNotFoundError(category_id)

        return category_orm

    def _orm_to_domain(self, category_orm: CategoryORM) -> Category:
        return Category(
            id=category_orm.id,
            name=category_orm.name,
            description=category_orm.description,
            is_active=category_orm.is_active,
            created_at=category_orm.created_at,
            updated_at=category_orm.updated_at,
        )
