from app.application.interfaces.repositories.comment_repository import (
    ICommentRepository,
)
from app.application.interfaces.repositories.ticket_repository import ITicketRepository
from app.domain.entities.comment import Comment


class ListCommentsUseCase:
    def __init__(
        self,
        comment_repository: ICommentRepository,
        ticket_repository: ITicketRepository,
    ) -> None:
        self._comment_repository = comment_repository
        self._ticket_repository = ticket_repository

    def execute(self, ticket_id: int) -> list[Comment]:

        self._ticket_repository.get_by_id(ticket_id)
        comments = self._comment_repository.list_by_ticket_id(ticket_id)

        return comments
