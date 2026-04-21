class DomainError(Exception):
    """Base class for expected application errors."""

    def __init__(
        self, message: str, status_code: int, errors: list[str] | None = None
    ) -> None:  # noqa: E501
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []


class NotFoundError(DomainError):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource_name: str, resource_id: int) -> None:
        message = f"{resource_name} with id {resource_id} was not found."
        super().__init__(message=message, status_code=404, errors=[message])


class BusinessValidationError(DomainError):
    """Raised when a business rule is violated outside Pydantic validation."""

    def __init__(self, message: str, errors: list[str] | None = None) -> None:
        super().__init__(message=message, status_code=400, errors=errors or [message])
