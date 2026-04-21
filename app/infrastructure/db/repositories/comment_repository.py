import copy
from datetime import UTC, datetime

from app.domain.entities.comment import Comment
from app.domain.exceptions.comment_exceptions import CommentNotFoundError
from app.infrastructure.db.repositories.memory_database import comment_db


class InMemoryCommentRepository:
    def _find_stored_comment_by_id_and_ticket_id(
        self, comment_id: int, ticket_id: int
    ) -> Comment:
        for comment in comment_db.comments:
            if comment.id != comment_id:
                continue

            if comment.ticket_id != ticket_id:
                raise CommentNotFoundError(comment_id)

            return comment

        raise CommentNotFoundError(comment_id)

    def _create(self, comment: Comment) -> Comment:
        comment_db.id_counter += 1
        comment.id = comment_db.id_counter

        comment.created_at = datetime.now(UTC)
        comment.updated_at = datetime.now(UTC)

        stored_comment = comment_db.add(comment)

        return copy.deepcopy(stored_comment)

    def _update(
        self, comment_id: int, ticket_id: int, updated_comment: Comment
    ) -> Comment:
        stored_comment = self._find_stored_comment_by_id_and_ticket_id(
            comment_id, ticket_id
        )

        stored_comment.content = updated_comment.content
        stored_comment.updated_at = datetime.now(UTC)

        return copy.deepcopy(stored_comment)

    def save(self, comment: Comment) -> Comment:
        if comment.id is None:
            return self._create(comment)
        else:
            return self._update(comment.id, comment.ticket_id, comment)

    def list_by_ticket_id(self, ticket_id: int) -> list[Comment]:
        comments = [
            comment for comment in comment_db.comments if comment.ticket_id == ticket_id
        ]
        return copy.deepcopy(comments)

    def get_by_id_and_ticket_id(self, comment_id: int, ticket_id: int) -> Comment:
        stored_comment = self._find_stored_comment_by_id_and_ticket_id(
            comment_id, ticket_id
        )
        return copy.deepcopy(stored_comment)
