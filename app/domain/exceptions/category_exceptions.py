from app.domain.exceptions.base_exceptions import NotFoundError


class CategoryNotFoundError(NotFoundError):
    def __init__(self, category_id: int) -> None:
        super().__init__(resource_name="Category", resource_id=category_id)
