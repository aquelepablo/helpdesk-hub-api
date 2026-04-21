from app.api.schemas.comment_schema import (
    CommentCreateRequest,
    CommentUpdateRequest,
)
from app.application.use_cases.comment.create_comment import CreateCommentInput
from app.application.use_cases.comment.update_comment import UpdateCommentInput


def to_create_comment_input(
    ticket_id: int, request: CommentCreateRequest
) -> CreateCommentInput:
    return CreateCommentInput(ticket_id=ticket_id, content=request.content)


def to_update_comment_input(
    comment_id: int, ticket_id: int, request: CommentUpdateRequest
) -> UpdateCommentInput:
    return UpdateCommentInput(
        comment_id=comment_id, ticket_id=ticket_id, content=request.content
    )
