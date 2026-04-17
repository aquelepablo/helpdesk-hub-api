import pytest
from pydantic import ValidationError

from app.adapters.http.schemas.ticket_schema import TicketUpdateRequest
from app.domain.enum.ticket_priority import TicketPriority


def test_update_ticket_schema_requires_at_least_one_field() -> None:
    with pytest.raises(ValidationError):
        TicketUpdateRequest(id=1)


def test_update_ticket_schema_rejects_non_positive_id() -> None:
    with pytest.raises(ValidationError):
        TicketUpdateRequest(id=0, priority=TicketPriority.URGENT)
