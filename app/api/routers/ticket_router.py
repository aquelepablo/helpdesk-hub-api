from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.api.docs.error_responses import (
    CREATE_RESPONSES,
    GET_BY_ID_RESPONSES,
    UPDATE_RESPONSES,
)
from app.api.mappers.pagination_mapper import to_pagination_params
from app.api.mappers.ticket_mapper import to_ticket_page_response
from app.api.messages.catalog import MessageKey, get_message
from app.api.schemas.common_schema import ApiResponse
from app.api.schemas.pagination_schema import PagedResponse, PageQuery
from app.api.schemas.ticket_schema import (
    TicketCreateRequest,
    TicketFilterRequest,
    TicketResponse,
    TicketUpdateRequest,
)
from app.application.use_cases.ticket.create_ticket import (
    CreateTicketInput,
    CreateTicketUseCase,
)
from app.application.use_cases.ticket.get_ticket_by_id import GetTicketByIdUseCase
from app.application.use_cases.ticket.list_tickets import (
    ListTicketsInput,
    ListTicketsUseCase,
)
from app.application.use_cases.ticket.update_ticket import (
    UpdateTicketInput,
    UpdateTicketUseCase,
)
from app.infrastructure.container import Container

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get(
    "",
    response_model=PagedResponse[TicketResponse],
    summary="Listar todos os tickets",
)
@inject
def list_tickets(
    filters: TicketFilterRequest = Depends(),
    page_query: PageQuery = Depends(),
    use_case: ListTicketsUseCase = Depends(Provide[Container.list_tickets_use_case]),
) -> PagedResponse[TicketResponse]:
    input_data = ListTicketsInput(
        pagination_params=to_pagination_params(page_query), **filters.model_dump()
    )

    tickets_page = use_case.execute(input_data)

    return to_ticket_page_response(
        message=get_message(MessageKey.TICKET_LISTED), page=tickets_page
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
    input_data = CreateTicketInput(**request.model_dump())
    new_ticket = use_case.execute(input_data)
    response = TicketResponse.model_validate(new_ticket)
    return ApiResponse(message=get_message(MessageKey.TICKET_CREATED), data=response)


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
    return ApiResponse(message=get_message(MessageKey.TICKET_RETRIEVED), data=response)


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
    input_data = UpdateTicketInput(ticket_id, **request.model_dump(exclude_unset=True))
    updated_ticket = use_case.execute(input_data)
    response = TicketResponse.model_validate(updated_ticket)
    return ApiResponse(message=get_message(MessageKey.TICKET_UPDATED), data=response)
