import pytest
from pydantic import ValidationError

from app.api.schemas.comment_schema import CommentCreateRequest


def test_create_comment_schema_accepts_valid_data() -> None:
    schema = CommentCreateRequest(content="A comment for testing purposes")

    assert schema.content == "A comment for testing purposes"


def test_create_comment_schema_rejects_blank_content() -> None:
    with pytest.raises(ValidationError):
        CommentCreateRequest(content="    ")


def test_create_comment_schema_rejects_extra_fields() -> None:
    payload: dict[str, object] = {
        "content": "A comment for testing purposes",
        "ticket_id": 1,
    }

    with pytest.raises(ValidationError):
        CommentCreateRequest.model_validate(payload)


def test_create_comment_schema_trims_content() -> None:
    schema = CommentCreateRequest(content="  A comment for testing purposes  ")

    assert schema.content == "A comment for testing purposes"


def test_create_comment_schema_rejects_missing_content() -> None:
    payload: dict[str, object] = {}

    with pytest.raises(ValidationError):
        CommentCreateRequest.model_validate(payload)
