"""Shared response models used across the API."""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standardized API response model."""

    success: bool = Field(
        default=True, description="Indicates whether the request succeeded."
    )
    message: str = Field(description="Human-friendly message that explains the result.")
    data: T = Field(description="Payload returned by the endpoint.")


class ErrorItem(BaseModel):
    code: str = Field(description="Machine-readable error code.")
    message: str = Field(description="Human-readable error message.")
    field: str | None = Field(
        default=None, description="The field that caused the error."
    )


class ErrorDetails(BaseModel):
    """Additional information about an API error."""

    errors: list[ErrorItem] = Field(default_factory=list)  # pyright: ignore[reportUnknownVariableType]


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""

    success: bool = Field(
        default=False, description="Indicates whether the request failed."
    )
    message: str = Field(description="High-level explanation of what went wrong.")
    details: ErrorDetails = Field(
        default_factory=ErrorDetails, description="Structured error details."
    )
