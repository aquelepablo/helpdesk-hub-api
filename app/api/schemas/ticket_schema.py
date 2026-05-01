from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from app.application.dtos.sorting import SortDirection
from app.domain.enum.ticket_priority import TicketPriority
from app.domain.enum.ticket_sort_field import TicketSortField
from app.domain.enum.ticket_status import TicketStatus


class TicketCreateRequest(BaseModel):
    model_config = {"extra": "forbid"}

    title: str = Field(
        ..., min_length=1, max_length=200, description="Short ticket name."
    )
    description: str = Field(
        ..., min_length=1, max_length=500, description="Optional ticket description."
    )
    category_id: int = Field(
        ..., gt=0, description="The ID of the category to which the ticket belongs."
    )
    priority: TicketPriority

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
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Description cannot be empty or blank.")
        return value.strip()


class TicketUpdateRequest(BaseModel):
    model_config = {"extra": "forbid"}

    category_id: int | None = Field(
        default=None,
        gt=0,
        description="The ID of the category to which the ticket belongs.",
    )
    priority: TicketPriority | None = None
    status: TicketStatus | None = None

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "TicketUpdateRequest":
        if all(
            value is None for value in (self.category_id, self.priority, self.status)
        ):
            raise ValueError("At least one field must be provided for update.")
        return self


class TicketFilterRequest(BaseModel):
    model_config = {"extra": "forbid"}

    status: TicketStatus | None = Field(
        default=None, description="Filter tickets by their status."
    )
    priority: TicketPriority | None = Field(
        default=None, description="Filter tickets by their priority."
    )
    category_id: int | None = Field(
        default=None,
        gt=0,
        description="The ID of the category to which the ticket belongs.",
    )
    sort_field: TicketSortField = Field(
        default=TicketSortField.ID, description="Field by which to sort the tickets."
    )
    sort_direction: SortDirection = Field(
        default=SortDirection.ASC, description="Direction in which to sort the tickets."
    )


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
