from fastapi import FastAPI

from app.adapters.http.routers import category_router, system_router
from app.infra.settings.project_metadata import project_metadata


def create_app() -> FastAPI:

    API_PREFIX = "/api/v1"

    app = FastAPI(
        title=project_metadata.title,
        description=project_metadata.description,
        version=project_metadata.version,
    )

    # TODO: Add middleware

    # TODO: Add Exceptions Handler

    app.include_router(system_router.router, prefix=API_PREFIX)
    app.include_router(category_router.router, prefix=API_PREFIX)

    return app


app = create_app()
