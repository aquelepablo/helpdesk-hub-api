from fastapi import status

from app.api.schemas.common_schema import ErrorResponse

CREATE_RESPONSES: dict[int, dict[str, type | str]] = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorResponse,
        "description": "Business rule violation.",
    },
    status.HTTP_422_UNPROCESSABLE_CONTENT: {
        "model": ErrorResponse,
        "description": "Request validation failed.",
    },
}

GET_BY_ID_RESPONSES: dict[int, dict[str, type | str]] = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorResponse,
        "description": "Resource not found.",
    },
    status.HTTP_422_UNPROCESSABLE_CONTENT: {
        "model": ErrorResponse,
        "description": "Request validation failed.",
    },
}

UPDATE_RESPONSES: dict[int, dict[str, type | str]] = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorResponse,
        "description": "Business rule violation.",
    },
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorResponse,
        "description": "Resource not found.",
    },
    status.HTTP_422_UNPROCESSABLE_CONTENT: {
        "model": ErrorResponse,
        "description": "Request validation failed.",
    },
}
