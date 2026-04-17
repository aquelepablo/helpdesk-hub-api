import pytest
from pydantic import ValidationError

from app.adapters.http.schemas.ticket_schema import TicketCreateRequest
from app.domain.enum.ticket_priority import TicketPriority


def test_create_ticket_schema_accepts_valid_data() -> None:
    schema = TicketCreateRequest(
        title="Test Ticket",
        description="A ticket for testing purposes",
        category_id=1,
        priority=TicketPriority.HIGH,
    )

    assert schema.title == "Test Ticket"
    assert schema.description == "A ticket for testing purposes"
    assert schema.category_id == 1
    assert schema.priority == TicketPriority.HIGH


def test_create_ticket_schema_rejects_blank_title() -> None:
    with pytest.raises(ValidationError):
        TicketCreateRequest(
            title="    ",
            description="A ticket with a blank title",
            category_id=1,
            priority=TicketPriority.HIGH,
        )


def test_create_ticket_schema_rejects_extra_fields() -> None:
    payload: dict[str, object] = {
        "title": "Test Ticket",
        "description": "A ticket for testing purposes",
        "category_id": 1,
        "priority": "high",
        "status": "closed",
    }

    with pytest.raises(ValidationError):
        TicketCreateRequest.model_validate(payload)
