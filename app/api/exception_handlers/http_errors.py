from fastapi import status

from app.api.schemas.common_schema import ErrorItem
from app.domain.exceptions.base_exceptions import (
    BusinessValidationError,
    DomainError,
    NotFoundError,
)


def map_domain_error_to_http(exc: DomainError) -> tuple[int, str, list[ErrorItem]]:
    if isinstance(exc, NotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
        error_code = "not_found"
    elif isinstance(exc, BusinessValidationError):
        status_code = status.HTTP_400_BAD_REQUEST
        error_code = "business_rule_violation"
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        error_code = "domain_error"

    errors = [
        ErrorItem(code=error_code, message=message, field=None)
        for message in exc.errors
    ]

    return status_code, exc.message, errors
