# Validar título, descrição, prioridade e categoria

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_status import TicketStatus


class TicketCreateRequest(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=255, description="Short ticket name."
    )
    description: str = Field(
        ..., min_length=1, max_length=500, description="Optional ticket description."
    )
    category_id: int = Field(
        ..., gt=0, description="The ID of the category to which the ticket belongs."
    )
    priority: TicketPriority
    status: TicketStatus = TicketStatus.OPEN

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Title cannot be empty or blank.")
        return cleaned_value

    @field_validator("description")
    @classmethod
    def validate_optional_description(cls, value: str) -> str:
        return value.strip()

    @field_validator("category_id")
    @classmethod
    def validate_category_id(cls, value: int | None) -> int | None:
        if value is None:
            raise ValueError("Category ID must be informed.")
        if value <= 0:
            raise ValueError("Category ID must be a positive integer.")
        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: TicketPriority | None) -> TicketPriority | None:
        if value is None:
            raise ValueError("Priority must be informed.")
        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: TicketPriority | None) -> TicketPriority | None:
        if value is None:
            raise ValueError("Status must be informed.")
        return value


class TicketUpdateRequest(BaseModel):
    id: int = Field(..., description="The ID of the ticket to update.")
    title: str | None = Field(
        default=None, min_length=1, max_length=255, description="Short ticket name."
    )
    description: str | None = Field(
        default=None,
        min_length=0,
        max_length=500,
        description="Optional ticket description.",
    )
    category_id: int | None = Field(
        default=None,
        gt=0,
        description="The ID of the category to which the ticket belongs.",
    )
    priority: TicketPriority | None = None
    status: TicketStatus | None = None

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Ticket ID must be a positive integer.")
        return value

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return value.strip()

    @field_validator("category_id")
    @classmethod
    def validate_category_id(cls, value: int | None) -> int | None:
        if value is None:
            return value
        if value <= 0:
            raise ValueError("Category ID must be a positive integer.")
        return value

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "TicketUpdateRequest":
        if all(
            value is None
            for value in (
                self.title,
                self.description,
                self.category_id,
                self.priority,
                self.status,
            )
        ):
            raise ValueError("At least one field must be provided for update.")
        return self


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    category_id: int
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
