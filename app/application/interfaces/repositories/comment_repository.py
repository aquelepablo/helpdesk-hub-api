from abc import ABC, abstractmethod

from app.domain.entities.comment import Comment


class ICommentRepository(ABC):
    @abstractmethod
    def create(self, comment: Comment) -> Comment: ...

    @abstractmethod
    def update(self, updated_comment: Comment) -> Comment: ...

    @abstractmethod
    def list_by_ticket_id(self, ticket_id: int) -> list[Comment]: ...

    @abstractmethod
    def get_by_id_and_ticket_id(self, comment_id: int, ticket_id: int) -> Comment: ...
