from dataclasses import dataclass

from app.application.ports.comment_repository import CommentRepository
from app.application.ports.ticket_repository import TicketRepository
from app.domain.entities.comment import Comment


@dataclass(slots=True)
class CreateCommentInput:
    ticket_id: int
    content: str


class CreateCommentUseCase:
    def __init__(
        self, comment_repository: CommentRepository, ticket_repository: TicketRepository
    ) -> None:
        self._comment_repository = comment_repository
        self._ticket_repository = ticket_repository

    def execute(self, input_data: CreateCommentInput) -> Comment:

        self._ticket_repository.get_by_id(input_data.ticket_id)

        new_comment = Comment(
            ticket_id=input_data.ticket_id, content=input_data.content
        )

        persisted_comment: Comment = self._comment_repository.save(new_comment)

        return persisted_comment
