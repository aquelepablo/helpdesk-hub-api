from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.api.docs.error_responses import (
    CREATE_RESPONSES,
    UPDATE_RESPONSES,
)
from app.api.mappers.comment_mapper import (
    to_create_comment_input,
    to_update_comment_input,
)
from app.api.schemas.comment_schema import (
    CommentCreateRequest,
    CommentResponse,
    CommentUpdateRequest,
)
from app.api.schemas.common_schema import ApiResponse
from app.application.use_cases.comment.create_comment import CreateCommentUseCase
from app.application.use_cases.comment.list_comments import ListCommentsUseCase
from app.application.use_cases.comment.update_comment import UpdateCommentUseCase
from app.infrastructure.container import Container

router = APIRouter(prefix="/ticket/{ticket_id}/comment", tags=["comment"])


@router.get(
    "",
    response_model=ApiResponse[list[CommentResponse]],
    summary="Listar todos os comentários de um ticket",
)
@inject
def list_comments(
    ticket_id: int,
    use_case: ListCommentsUseCase = Depends(Provide[Container.list_comments_use_case]),
) -> ApiResponse[list[CommentResponse]]:
    comments = use_case.execute(ticket_id)
    responses = [CommentResponse.model_validate(comment) for comment in comments]
    return ApiResponse(
        message="Listagem de comentários realizada com sucesso", data=responses
    )


@router.post(
    "",
    response_model=ApiResponse[CommentResponse],
    status_code=status.HTTP_201_CREATED,
    responses={**CREATE_RESPONSES},
)
@inject
def create_comment(
    ticket_id: int,
    request: CommentCreateRequest,
    use_case: CreateCommentUseCase = Depends(
        Provide[Container.create_comment_use_case]
    ),
) -> ApiResponse[CommentResponse]:
    input_data = to_create_comment_input(ticket_id, request)
    new_comment = use_case.execute(input_data)
    response = CommentResponse.model_validate(new_comment)
    return ApiResponse(message="Comentário criado com sucesso", data=response)


@router.patch(
    "/{comment_id}",
    response_model=ApiResponse[CommentResponse],
    summary="Atualizar detalhes de um comentário",
    responses={**UPDATE_RESPONSES},
)
@inject
def update_comment(
    ticket_id: int,
    comment_id: int,
    request: CommentUpdateRequest,
    use_case: UpdateCommentUseCase = Depends(
        Provide[Container.update_comment_use_case]
    ),
) -> ApiResponse[CommentResponse]:
    input_data = to_update_comment_input(comment_id, ticket_id, request)
    updated_comment = use_case.execute(input_data)
    response = CommentResponse.model_validate(updated_comment)
    return ApiResponse(message="Comentário atualizado com sucesso", data=response)
