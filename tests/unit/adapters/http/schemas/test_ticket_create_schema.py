import pytest
from pydantic import ValidationError

from app.adapters.http.schemas.ticket_schema import TicketCreateRequest
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_status import TicketStatus


def test_create_ticket_schema_accepts_valid_data() -> None:
    schema = TicketCreateRequest(
        title="Test Ticket",
        description="A ticket for testing purposes",
        category_id=1,
        priority=TicketPriority.HIGH,
        status=TicketStatus.OPEN,
    )

    assert schema.title == "Test Ticket"
    assert schema.description == "A ticket for testing purposes"
    assert schema.category_id == 1
    assert schema.priority == TicketPriority.HIGH
    assert schema.status == TicketStatus.OPEN


def test_create_ticket_schema_rejects_blank_title() -> None:
    with pytest.raises(ValidationError):
        TicketCreateRequest(
            title="    ",
            description="A ticket with a blank title",
            category_id=1,
            priority=TicketPriority.HIGH,
            status=TicketStatus.OPEN,
        )
