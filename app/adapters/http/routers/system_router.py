from datetime import datetime

from fastapi import APIRouter

from app.infra.settings.settings import settings

router = APIRouter(tags=["System"])


@router.get(
    "/",
    summary="Endpoint de entrada",
)
def get_root() -> str:
    return "HelpDesk Hub API online"


@router.get(
    "/health",
    summary="Apresentar saúde atual da API",
)
def get_health() -> dict[str, str]:
    return {"status": "ok"}


@router.get(
    "/info",
    summary="Apresentar informações da API",
)
def get_info() -> dict[str, str]:
    api_info = {
        "service": settings.app_name,
        "version": settings.app_version,
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
