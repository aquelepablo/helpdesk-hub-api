from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapters.http.routers import category_router, system_router, ticket_router
from app.infra.bootstrap.seed_categories import seed_categories
from app.infra.settings.project_metadata import project_metadata

API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    seed_categories()
    yield


def create_app() -> FastAPI:

    app = FastAPI(
        title=project_metadata.title,
        description=project_metadata.description,
        version=project_metadata.version,
        lifespan=lifespan,
    )

    # TODO: Add middleware

    # TODO: Add Exceptions Handler

    app.include_router(system_router.router, prefix=API_PREFIX)
    app.include_router(category_router.router, prefix=API_PREFIX)
    app.include_router(ticket_router.router, prefix=API_PREFIX)

    return app


app = create_app()
