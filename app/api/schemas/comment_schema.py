from datetime import datetime

from pydantic import BaseModel, Field, field_validator

MAX_COMMENT_LENGTH = 500


def validate_comment_content(value: str) -> str:
    cleaned_value = value.strip()
    if not cleaned_value:
        raise ValueError("Comment cannot be empty or blank.")
    return cleaned_value


class CommentCreateRequest(BaseModel):
    model_config = {"extra": "forbid"}

    content: str = Field(
        ...,
        min_length=1,
        max_length=MAX_COMMENT_LENGTH,
        description="Comment's content.",
    )

    _validade_content = field_validator("content")(validate_comment_content)


class CommentUpdateRequest(BaseModel):
    model_config = {"extra": "forbid"}

    content: str = Field(
        ...,
        min_length=1,
        max_length=MAX_COMMENT_LENGTH,
        description="Comment's content.",
    )

    _validade_content = field_validator("content")(validate_comment_content)


class CommentResponse(BaseModel):
    id: int
    ticket_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
