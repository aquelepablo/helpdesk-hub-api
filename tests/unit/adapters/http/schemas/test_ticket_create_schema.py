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


def test_create_ticket_schema_trims_title_and_description() -> None:
    schema = TicketCreateRequest(
        title="  Test Ticket  ",
        description="  A ticket for testing purposes  ",
        category_id=1,
        priority=TicketPriority.HIGH,
    )

    assert schema.title == "Test Ticket"
    assert schema.description == "A ticket for testing purposes"


def test_create_ticket_schema_rejects_blank_description() -> None:
    with pytest.raises(ValidationError):
        TicketCreateRequest(
            title="Test Ticket",
            description="   ",
            category_id=1,
            priority=TicketPriority.HIGH,
        )


def test_create_ticket_schema_rejects_non_positive_category_id() -> None:
    with pytest.raises(ValidationError):
        TicketCreateRequest(
            title="Test Ticket",
            description="A ticket for testing purposes",
            category_id=0,
            priority=TicketPriority.HIGH,
        )


def test_create_ticket_schema_rejects_invalid_priority() -> None:
    payload: dict[str, object] = {
        "title": "Test Ticket",
        "description": "A ticket for testing purposes",
        "category_id": 1,
        "priority": "invalid",
    }

    with pytest.raises(ValidationError):
        TicketCreateRequest.model_validate(payload)
