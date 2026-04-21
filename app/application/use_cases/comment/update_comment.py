from dataclasses import dataclass

from app.application.ports.comment_repository import (
    CommentRepository,
)
from app.domain.entities.comment import Comment


@dataclass(slots=True)
class UpdateCommentInput:
    comment_id: int
    ticket_id: int
    content: str


class UpdateCommentUseCase:
    def __init__(self, comment_repository: CommentRepository) -> None:
        self._comment_repo = comment_repository

    def execute(self, input_data: UpdateCommentInput) -> Comment:

        existing_comment = self._comment_repo.get_by_id_and_ticket_id(
            input_data.comment_id, input_data.ticket_id
        )

        existing_comment.content = input_data.content

        return self._comment_repo.save(existing_comment)
