from enum import Enum


class TicketSortField(Enum):
    """Represents the fields by which tickets can be sorted"""

    ID = "id"
    TITLE = "title"
    PRIORITY = "priority"
    STATUS = "status"
