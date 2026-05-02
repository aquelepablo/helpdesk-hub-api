from dataclasses import dataclass

from app.application.interfaces.repositories.comment_repository import CommentRepository
from app.application.interfaces.repositories.ticket_repository import ITicketRepository
from app.domain.entities.comment import Comment


@dataclass(slots=True)
class UpdateCommentInput:
    comment_id: int
    ticket_id: int
    content: str


class UpdateCommentUseCase:
    def __init__(
        self,
        comment_repository: CommentRepository,
        ticket_repository: ITicketRepository,
    ) -> None:
        self._comment_repository = comment_repository
        self._ticket_repository = ticket_repository

    def execute(self, input_data: UpdateCommentInput) -> Comment:

        self._ticket_repository.get_by_id(input_data.ticket_id)
        existing_comment = self._comment_repository.get_by_id_and_ticket_id(
            input_data.comment_id, input_data.ticket_id
        )

        existing_comment.content = input_data.content

        return self._comment_repository.update(existing_comment)
