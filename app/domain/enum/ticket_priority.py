from enum import Enum


class TicketPriority(Enum):
    """Represents the priority of a ticket"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
