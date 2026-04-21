from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.api.docs.error_responses import (
    CREATE_RESPONSES,
    GET_BY_ID_RESPONSES,
    UPDATE_RESPONSES,
)
from app.api.mappers.ticket_mapper import (
    to_create_ticket_input,
    to_update_ticket_input,
)
from app.api.schemas.common_schema import ApiResponse
from app.api.schemas.ticket_schema import (
    TicketCreateRequest,
    TicketResponse,
    TicketUpdateRequest,
)
from app.application.use_cases.ticket.create_ticket import CreateTicketUseCase
from app.application.use_cases.ticket.get_ticket_by_id import GetTicketByIdUseCase
from app.application.use_cases.ticket.list_tickets import ListTicketsUseCase
from app.application.use_cases.ticket.update_ticket import UpdateTicketUseCase
from app.infrastructure.container import Container

router = APIRouter(prefix="/ticket", tags=["tickets"])


@router.get(
    "",
    response_model=ApiResponse[list[TicketResponse]],
    summary="Listar todos os tickets",
)
@inject
def list_tickets(
    use_case: ListTicketsUseCase = Depends(Provide[Container.list_tickets_use_case]),
) -> ApiResponse[list[TicketResponse]]:
    tickets = use_case.execute()
    responses = [TicketResponse.model_validate(ticket) for ticket in tickets]
    return ApiResponse(
        message="Listagem de tickets realizada com sucesso", data=responses
    )


@router.post(
    "",
    response_model=ApiResponse[TicketResponse],
    status_code=status.HTTP_201_CREATED,
    responses={**CREATE_RESPONSES},
)
@inject
def create_ticket(
    request: TicketCreateRequest,
    use_case: CreateTicketUseCase = Depends(Provide[Container.create_ticket_use_case]),
) -> ApiResponse[TicketResponse]:
    input_data = to_create_ticket_input(request)
    new_ticket = use_case.execute(input_data)
    response = TicketResponse.model_validate(new_ticket)
    return ApiResponse(message="Ticket criado com sucesso", data=response)


@router.get(
    "/{ticket_id}",
    response_model=ApiResponse[TicketResponse],
    summary="Obter detalhes de um ticket",
    responses={**GET_BY_ID_RESPONSES},
)
@inject
def get_ticket_by_id(
    ticket_id: int,
    use_case: GetTicketByIdUseCase = Depends(
        Provide[Container.get_ticket_by_id_use_case]
    ),  # noqa: E501
) -> ApiResponse[TicketResponse]:
    ticket = use_case.execute(ticket_id)
    response = TicketResponse.model_validate(ticket)
    return ApiResponse(message="Detalhes do ticket obtidos com sucesso", data=response)


@router.patch(
    "/{ticket_id}",
    response_model=ApiResponse[TicketResponse],
    summary="Atualizar detalhes de um ticket",
    responses={**UPDATE_RESPONSES},
)
@inject
def update_ticket(
    ticket_id: int,
    request: TicketUpdateRequest,
    use_case: UpdateTicketUseCase = Depends(Provide[Container.update_ticket_use_case]),
) -> ApiResponse[TicketResponse]:
    input_data = to_update_ticket_input(request)
    updated_ticket = use_case.execute(ticket_id, input_data)
    response = TicketResponse.model_validate(updated_ticket)
    return ApiResponse(message="Ticket atualizado com sucesso", data=response)
