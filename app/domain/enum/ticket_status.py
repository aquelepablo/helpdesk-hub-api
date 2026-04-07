from enum import Enum


class TicketStatus(Enum):
    """Represents the status of a ticket"""

    OPEN = "open"
    CLOSED = "closed"
