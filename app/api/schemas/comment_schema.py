from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class CommentCreateRequest(BaseModel):
    model_config = {"extra": "forbid"}

    content: str = Field(
        ..., min_length=1, max_length=500, description="Comment's content."
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Comment cannot be empty or blank.")
        return cleaned_value


class CommentUpdateRequest(BaseModel):
    model_config = {"extra": "forbid"}

    content: str = Field(
        ..., min_length=1, max_length=500, description="Comment's content."
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        cleaned_value = value.strip()
        if not cleaned_value:
            raise ValueError("Comment cannot be empty or blank.")
        return cleaned_value


class CommentResponse(BaseModel):
    id: int
    ticket_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
