from app.application.interfaces.repositories.comment_repository import (
    CommentRepository,
)
from app.application.interfaces.repositories.ticket_repository import TicketRepository
from app.domain.entities.comment import Comment


class ListCommentsUseCase:
    def __init__(
        self, comment_repository: CommentRepository, ticket_repository: TicketRepository
    ) -> None:
        self._comment_repository = comment_repository
        self._ticket_repository = ticket_repository

    def execute(self, ticket_id: int) -> list[Comment]:

        self._ticket_repository.get_by_id(ticket_id)
        comments = self._comment_repository.list_by_ticket_id(ticket_id)

        return comments
