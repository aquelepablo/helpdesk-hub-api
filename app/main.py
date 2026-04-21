from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exception_handlers.handlers import register_exception_handlers
from app.api.routers import category_router, system_router, ticket_router
from app.infrastructure.bootstrap.seed_categories import seed_categories
from app.infrastructure.container import Container
from app.infrastructure.settings.project_metadata import project_metadata

API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    seed_categories()
    yield


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    This function sets up the application with necessary configurations, including

    Returns:
        FastAPI: An instance of the FastAPI application ready to be run.
    """
    container = Container()
    container.wire(modules=[category_router, ticket_router])

    app = FastAPI(
        title=project_metadata.title,
        description=project_metadata.description,
        version=project_metadata.version,
        lifespan=lifespan,
    )

    # TODO: Add middleware

    register_exception_handlers(app)

    app.include_router(system_router.router, prefix=API_PREFIX)
    app.include_router(category_router.router, prefix=API_PREFIX)
    app.include_router(ticket_router.router, prefix=API_PREFIX)

    return app


app = create_app()
