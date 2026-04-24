from enum import Enum


class TicketPriority(Enum):
    """Represents the priority of a ticket"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

    @property
    def sort_order(self) -> int:
        order = {
            TicketPriority.LOW: 1,
            TicketPriority.MEDIUM: 2,
            TicketPriority.HIGH: 3,
            TicketPriority.URGENT: 4,
        }
        return order[self]
