import pytest
from pydantic import ValidationError

from app.adapters.http.schemas.ticket_schema import TicketUpdateRequest
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_status import TicketStatus


def test_update_ticket_schema_requires_at_least_one_field() -> None:
    with pytest.raises(ValidationError):
        TicketUpdateRequest()


def test_update_ticket_schema_accepts_only_category_id() -> None:
    schema = TicketUpdateRequest(category_id=1)

    assert schema.category_id == 1
    assert schema.priority is None
    assert schema.status is None


def test_update_ticket_schema_accepts_only_priority() -> None:
    schema = TicketUpdateRequest(priority=TicketPriority.URGENT)

    assert schema.category_id is None
    assert schema.priority == TicketPriority.URGENT
    assert schema.status is None


def test_update_ticket_schema_accepts_only_status() -> None:
    schema = TicketUpdateRequest(status=TicketStatus.CLOSED)

    assert schema.category_id is None
    assert schema.priority is None
    assert schema.status == TicketStatus.CLOSED


def test_update_ticket_schema_rejects_non_positive_category_id() -> None:
    with pytest.raises(ValidationError):
        TicketUpdateRequest(category_id=0)


def test_update_ticket_schema_rejects_extra_fields() -> None:
    payload: dict[str, object] = {
        "priority": "high",
        "title": "Invalid extra field",
    }

    with pytest.raises(ValidationError):
        TicketUpdateRequest.model_validate(payload)


def test_update_ticket_schema_rejects_id_in_body() -> None:
    payload: dict[str, object] = {
        "id": 1,
        "name": "Updated ticket",
    }

    with pytest.raises(ValidationError):
        TicketUpdateRequest.model_validate(payload)
