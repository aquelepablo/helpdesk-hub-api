from app.adapters.http.schemas.ticket_schema import (
    TicketCreateRequest,
    TicketUpdateRequest,
)
from app.application.use_cases.ticket.create_ticket import CreateTicketInput
from app.application.use_cases.ticket.update_ticket import UpdateTicketInput


def to_create_ticket_input(request: TicketCreateRequest) -> CreateTicketInput:
    return CreateTicketInput(
        title=request.title,
        description=request.description,
        category_id=request.category_id,
        priority=request.priority,
    )


def to_update_ticket_input(request: TicketUpdateRequest) -> UpdateTicketInput:
    return UpdateTicketInput(
        category_id=request.category_id,
        priority=request.priority,
        status=request.status,
    )
