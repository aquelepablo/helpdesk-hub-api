from datetime import UTC, datetime

from app.application.interfaces.repositories.comment_repository import (
    ICommentRepository,
)
from app.domain.entities.comment import Comment
from app.domain.exceptions.comment_exceptions import CommentNotFoundError
from app.infrastructure.db.repositories.memory.memory_database import comment_db
from app.infrastructure.db.repositories.memory.safe_copy import detached_copy


class InMemoryCommentRepository(ICommentRepository):
    def create(self, comment: Comment) -> Comment:
        comment_db.id_counter += 1
        comment.id = comment_db.id_counter

        comment.created_at = datetime.now(UTC)
        comment.updated_at = datetime.now(UTC)

        stored_comment = comment_db.add(comment)

        return detached_copy(stored_comment)

    def update(self, updated_comment: Comment) -> Comment:
        if not updated_comment.id or updated_comment.id <= 0:
            raise ValueError("Comment must have a valid ID")

        stored_comment = self._find_stored_comment(
            updated_comment.id, updated_comment.ticket_id
        )

        stored_comment.content = updated_comment.content
        stored_comment.updated_at = datetime.now(UTC)

        return detached_copy(stored_comment)

    def list_by_ticket_id(self, ticket_id: int) -> list[Comment]:
        comments = [
            comment for comment in comment_db.comments if comment.ticket_id == ticket_id
        ]
        return detached_copy(comments)

    def get_by_id_and_ticket_id(self, comment_id: int, ticket_id: int) -> Comment:
        stored_comment = self._find_stored_comment(comment_id, ticket_id)
        return detached_copy(stored_comment)

    # ========== Private methods ==========
    def _find_stored_comment(self, comment_id: int, ticket_id: int) -> Comment:
        for comment in comment_db.comments:
            if comment.id != comment_id:
                continue

            if comment.ticket_id != ticket_id:
                raise CommentNotFoundError(comment_id)

            return comment

        raise CommentNotFoundError(comment_id)
