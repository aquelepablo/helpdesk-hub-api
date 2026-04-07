from datetime import datetime

from fastapi import APIRouter

from app.infra.settings.project_metadata import project_metadata
from app.infra.settings.settings import settings

router = APIRouter(tags=["System"])


@router.get(
    "/",
    summary="Endpoint de entrada",
)
def get_root() -> dict[str, str]:
    return {
        "service": project_metadata.title,
        "description": project_metadata.description,
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
        "service": project_metadata.title,
        "project_name": project_metadata.name,
        "version": project_metadata.version,
        "environment": settings.app_env,
    }
    return api_info


@router.get(
    "/ping",
    summary="Retornar a hora atual da API",
)
def get_ping() -> dict[str, str]:
    dt_now = datetime.now()
    return {"timestamp": dt_now.isoformat()}
