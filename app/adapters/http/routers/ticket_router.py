from fastapi import APIRouter, status

from app.adapters.http.mappers.ticket_mapper import (
    to_create_ticket_input,
    to_update_ticket_input,
)
from app.adapters.http.schemas.common_schema import ApiResponse
from app.adapters.http.schemas.ticket_schema import (
    TicketCreateRequest,
    TicketResponse,
    TicketUpdateRequest,
)
from app.application.use_cases.ticket.create_ticket import CreateTicketUseCase
from app.application.use_cases.ticket.get_ticket_by_id import GetTicketByIdUseCase
from app.application.use_cases.ticket.list_tickets import ListTicketsUseCase
from app.application.use_cases.ticket.update_ticket import UpdateTicketUseCase
from app.domain.repositories.ticket_repository import TicketRepository
from app.infra.db.repositories.ticket_repository import InMemoryTicketRepository

router = APIRouter(prefix="/ticket", tags=["tickets"])


def _get_ticket_repository() -> TicketRepository:
    return InMemoryTicketRepository()


@router.get(
    "",
    response_model=ApiResponse[list[TicketResponse]],
    summary="Listar todos os tickets",
)
def list_tickets() -> ApiResponse[list[TicketResponse]]:
    list_tickets_use_case = ListTicketsUseCase(_get_ticket_repository())
    tickets = list_tickets_use_case.execute()
    responses = [TicketResponse.model_validate(ticket) for ticket in tickets]

    return ApiResponse(
        message="Listagem de tickets realizada com sucesso", data=responses
    )


@router.post(
    "",
    response_model=ApiResponse[TicketResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(request: TicketCreateRequest) -> ApiResponse[TicketResponse]:
    input_data = to_create_ticket_input(request)

    create_ticket_use_case = CreateTicketUseCase(_get_ticket_repository())
    new_ticket = create_ticket_use_case.execute(input_data)

    response = TicketResponse.model_validate(new_ticket)
    return ApiResponse(message="Ticket criado com sucesso", data=response)


# TODO: Implement Exception Handler to return 404 on not found
@router.get(
    "/{ticket_id}",
    response_model=ApiResponse[TicketResponse],
    summary="Obter detalhes de um ticket",
)
def get_ticket_by_id(ticket_id: int) -> ApiResponse[TicketResponse]:
    get_ticket_by_id_use_case = GetTicketByIdUseCase(_get_ticket_repository())
    ticket = get_ticket_by_id_use_case.execute(ticket_id)
    response = TicketResponse.model_validate(ticket)

    return ApiResponse(message="Detalhes do ticket obtidos com sucesso", data=response)


@router.patch(
    "",
    response_model=ApiResponse[TicketResponse],
    summary="Atualizar detalhes de um ticket",
)
def update_ticket(request: TicketUpdateRequest) -> ApiResponse[TicketResponse]:
    input_data = to_update_ticket_input(request)
    update_ticket_use_case = UpdateTicketUseCase(_get_ticket_repository())
    updated_ticket = update_ticket_use_case.execute(input_data)
    response = TicketResponse.model_validate(updated_ticket)
    return ApiResponse(message="Ticket atualizado com sucesso", data=response)
