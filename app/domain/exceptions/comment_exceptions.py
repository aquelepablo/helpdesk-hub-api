from app.domain.exceptions.base_exceptions import NotFoundError


class CommentNotFoundError(NotFoundError):
    def __init__(self, comment_id: int) -> None:
        super().__init__(resource_name="Comment", resource_id=comment_id)
