import logging
from typing import cast

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.exception_handlers.http_errors import map_domain_error_to_http
from app.api.schemas.common_schema import (
    ErrorDetails,
    ErrorItem,
    ErrorResponse,
)
from app.domain.exceptions.base_exceptions import DomainError

logger = logging.getLogger(__name__)


def _build_error_response(
    status_code: int, message: str, errors: list[ErrorItem]
) -> JSONResponse:
    """Create a JSONResponse using the standard error format."""

    payload = ErrorResponse(message=message, details=ErrorDetails(errors=errors))
    return JSONResponse(status_code=status_code, content=payload.model_dump())


async def handle_domain_error(_: Request, exc: Exception) -> JSONResponse:
    """Handle domain-specific errors created by the application."""
    domain_exc = cast(DomainError, exc)

    status_code, message, errors = map_domain_error_to_http(domain_exc)

    return _build_error_response(
        status_code=status_code, message=message, errors=errors
    )


async def handle_request_validation_error(_: Request, exc: Exception) -> JSONResponse:
    """Handle invalid request bodies, params, and types."""
    request_exc = cast(RequestValidationError, exc)

    errors: list[ErrorItem] = []
    for error in request_exc.errors():
        field_path = " -> ".join(str(item) for item in error["loc"] if item != "body")
        errors.append(
            ErrorItem(
                code=error["type"],
                message=error["msg"],
                field=field_path or None,
            )
        )

    return _build_error_response(
        message="Request validation failed.",
        errors=errors,
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )


# TODO: Send log do infra
async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected errors without leaking internal details."""
    logger.exception("Unexpected error while handling request")

    return _build_error_response(
        message="An unexpected error occurred.",
        errors=[
            ErrorItem(
                code="unexpected_error",
                message="Internal server error.",
                field=None,
            )
        ],
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all global exception handlers on the FastAPI app."""
    app.add_exception_handler(DomainError, handle_domain_error)
    app.add_exception_handler(RequestValidationError, handle_request_validation_error)
    app.add_exception_handler(Exception, handle_unexpected_error)
