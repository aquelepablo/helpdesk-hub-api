from enum import StrEnum


class TicketSortField(StrEnum):
    """Represents the fields by which tickets can be sorted"""

    ID = "id"
    TITLE = "title"
    PRIORITY = "priority"
    STATUS = "status"
