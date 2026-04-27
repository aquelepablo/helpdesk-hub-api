from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exception_handlers.handlers import register_exception_handlers
from app.api.routers import (
    category_router,
    comment_router,
    system_router,
    ticket_router,
)
from app.infrastructure.bootstrap.seed_categories import seed_categories
from app.infrastructure.container import Container
from app.infrastructure.logging.logging_config import configure_logging

# from app.infrastructure.settings.project_metadata import project_metadata
from app.infrastructure.settings.settings import settings

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
    configure_logging()

    container = Container()
    container.wire(modules=[category_router, ticket_router, comment_router])

    app = FastAPI(
        title=settings.project_title,
        description=settings.project_description,
        version=settings.project_version,
        lifespan=lifespan,
    )

    # TODO: Add middleware

    register_exception_handlers(app)

    app.include_router(system_router.router, prefix=API_PREFIX)
    app.include_router(category_router.router, prefix=API_PREFIX)
    app.include_router(ticket_router.router, prefix=API_PREFIX)
    app.include_router(comment_router.router, prefix=API_PREFIX)

    return app


app = create_app()
