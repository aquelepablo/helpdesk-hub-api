from app.application.interfaces.repositories.comment_repository import (
    ICommentRepository,
)
from app.domain.entities.comment import Comment
from app.domain.exceptions.comment_exceptions import CommentNotFoundError
from app.infrastructure.db.sqlalchemy.models import CommentORM
from sqlalchemy import select
from sqlalchemy.orm import Session


class SQLAlchemyCommentRepository(ICommentRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, comment: Comment) -> Comment:

        if not comment:
            raise ValueError("Comment cannot be None")

        comment_orm = CommentORM(
            content=comment.content,
            ticket_id=comment.ticket_id,
        )

        self._session.add(comment_orm)
        self._session.commit()
        self._session.refresh(comment_orm)

        return self._orm_to_domain(comment_orm)

    def update(self, updated_comment: Comment) -> Comment:

        if not updated_comment.id or updated_comment.id <= 0:
            raise ValueError("Comment must have a valid ID")

        comment_orm = self._get_comment_orm(
            updated_comment.id, updated_comment.ticket_id
        )

        comment_orm.content = updated_comment.content

        self._session.commit()
        self._session.refresh(comment_orm)

        return self._orm_to_domain(comment_orm)

    def list_by_ticket_id(self, ticket_id: int) -> list[Comment]:
        comments_orm = self._session.scalars(
            select(CommentORM).where(CommentORM.ticket_id == ticket_id)
        ).all()

        return [self._orm_to_domain(comment_orm) for comment_orm in comments_orm]

    def get_by_id_and_ticket_id(self, comment_id: int, ticket_id: int) -> Comment:
        comment_orm = self._get_comment_orm(comment_id, ticket_id)

        return self._orm_to_domain(comment_orm)

    # ========== Private methods ==========
    def _get_comment_orm(self, comment_id: int, ticket_id: int) -> CommentORM:

        comment_orm = self._session.scalars(
            select(CommentORM).where(
                CommentORM.id == comment_id, CommentORM.ticket_id == ticket_id
            )
        ).one_or_none()

        if comment_orm is None:
            raise CommentNotFoundError(comment_id)

        return comment_orm

    def _orm_to_domain(self, comment_orm: CommentORM) -> Comment:
        return Comment(
            id=comment_orm.id,
            content=comment_orm.content,
            ticket_id=comment_orm.ticket_id,
            created_at=comment_orm.created_at,
            updated_at=comment_orm.updated_at,
        )
