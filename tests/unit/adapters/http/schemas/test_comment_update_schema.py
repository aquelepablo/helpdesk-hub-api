import pytest
from pydantic import ValidationError

from app.api.schemas.comment_schema import CommentUpdateRequest


def test_update_comment_schema_accepts_valid_data() -> None:
    schema = CommentUpdateRequest(content="Updated comment")

    assert schema.content == "Updated comment"


def test_update_comment_schema_rejects_blank_content() -> None:
    with pytest.raises(ValidationError):
        CommentUpdateRequest(content="    ")


def test_update_comment_schema_rejects_extra_fields() -> None:
    payload: dict[str, object] = {
        "content": "Updated comment",
        "ticket_id": 1,
    }

    with pytest.raises(ValidationError):
        CommentUpdateRequest.model_validate(payload)


def test_update_comment_schema_rejects_id_in_body() -> None:
    payload: dict[str, object] = {
        "id": 1,
        "content": "Updated comment",
    }

    with pytest.raises(ValidationError):
        CommentUpdateRequest.model_validate(payload)


def test_update_comment_schema_trims_content() -> None:
    schema = CommentUpdateRequest(content="  Updated comment  ")

    assert schema.content == "Updated comment"
