from datetime import UTC, datetime

from fastapi import APIRouter

from app.infrastructure.settings.settings import settings

router = APIRouter(tags=["System"])


@router.get(
    "/",
    summary="Endpoint de entrada",
)
def get_root() -> dict[str, str]:
    return {
        "service": settings.project_title,
        "description": settings.project_description,
    }


@router.get(
    "/live",
    summary="Indica se o serviço está online",
)
def get_liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get(
    "/health",
    summary="Apresentar saúde atual da API",
)
def get_health() -> dict[str, str | list[str]]:
    return {
        "status": "ok",
        "checks": [],
    }


@router.get(
    "/info",
    summary="Apresentar informações da API",
)
def get_info() -> dict[str, str]:
    api_info = {
        "service": settings.project_title,
        "project_name": settings.project_name,
        "version": settings.project_version,
        "environment": settings.environment.value,
    }
    return api_info


@router.get(
    "/ping",
    summary="Retornar a hora atual da API",
)
def get_ping() -> dict[str, str]:
    dt_now = datetime.now(tz=UTC)

    return {"timestamp": dt_now.isoformat(), "timezone": "UTC"}
