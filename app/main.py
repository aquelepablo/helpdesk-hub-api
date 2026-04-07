from fastapi import FastAPI

from app.adapters.http.routers import system_router
from app.infra.settings.project_metadata import project_metadata

app = FastAPI(
    title=project_metadata.title,
    description=project_metadata.description,
    version=project_metadata.version,
)

app.include_router(system_router.router)
