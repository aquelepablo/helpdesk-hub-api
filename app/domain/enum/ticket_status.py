from enum import StrEnum


class TicketStatus(StrEnum):
    """Represents the status of a ticket"""

    OPEN = "open"
    CLOSED = "closed"

    @property
    def sort_order(self) -> int:
        order = {
            TicketStatus.OPEN: 1,
            TicketStatus.CLOSED: 2,
        }
        return order[self]
