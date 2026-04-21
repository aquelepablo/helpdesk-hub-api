from app.api.schemas.ticket_schema import (
    TicketCreateRequest,
    TicketFilterRequest,
    TicketUpdateRequest,
)
from app.application.use_cases.ticket.create_ticket import CreateTicketInput
from app.application.use_cases.ticket.list_tickets import ListTicketsInput
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


def to_list_ticket_input(request: TicketFilterRequest) -> ListTicketsInput:
    return ListTicketsInput(
        status=request.status,
        priority=request.priority,
        category_id=request.category_id,
    )
