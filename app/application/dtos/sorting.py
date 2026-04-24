from dataclasses import dataclass
from enum import Enum


class SortDirection(Enum):
    """Enumeration for sort directions."""

    ASC = "asc"
    DESC = "desc"


@dataclass
class OrderCriterion:
    field: str
    direction: SortDirection
