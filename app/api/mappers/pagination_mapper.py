from app.api.schemas.pagination_schema import PageQuery
from app.application.dtos.pagination import PaginationParams


def to_pagination_params(request: PageQuery) -> PaginationParams:
    return PaginationParams(page=request.page, page_size=request.page_size)
