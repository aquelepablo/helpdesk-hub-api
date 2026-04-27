import copy
from typing import TypeVar

T = TypeVar("T")


def detached_copy(value: T) -> T:
    """
    Return a copy detached from the in-memory store.

    Memory repositories keep mutable dataclass instances in module-level lists.
    Returning a copy prevents callers from mutating stored state by accident.
    This helper should not be needed when persistence moves to a real database/ORM.
    """

    return copy.deepcopy(value)
