from app.api.schemas.pagination_schema import PagedResponse
from app.api.schemas.ticket_schema import (
    TicketResponse,
)
from app.application.dtos.pagination import PagedResult
from app.domain.entities.ticket import Ticket


def to_ticket_response(ticket: Ticket) -> TicketResponse:
    return TicketResponse.model_validate(ticket)


def to_ticket_page_response(
    message: str, page: PagedResult[Ticket]
) -> PagedResponse[TicketResponse]:
    return PagedResponse(
        message=message,
        items=[to_ticket_response(ticket) for ticket in page.items],
        total_items=page.total_items,
        page=page.page,
        page_size=page.page_size,
        total_pages=page.total_pages,
    )
