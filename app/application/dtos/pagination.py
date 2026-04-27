from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

# TODO: search cross cutting
# TODO: think about put pagination math here and take out of infra.


@dataclass(frozen=True, slots=True)
class PaginationParams:
    page: int
    page_size: int

    @property
    def offset(self) -> int:

        return (self.page - 1) * self.page_size


@dataclass(frozen=True, slots=True)
class PagedResult(Generic[T]):
    items: list[T]
    total_items: int
    page: int
    page_size: int
    total_pages: int
