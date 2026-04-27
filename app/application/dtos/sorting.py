from dataclasses import dataclass
from enum import StrEnum


class SortDirection(StrEnum):
    """Enumeration for sort directions."""

    ASC = "asc"
    DESC = "desc"


@dataclass
class OrderCriterion:
    field: str
    direction: SortDirection
