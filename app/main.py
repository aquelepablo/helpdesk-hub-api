from fastapi import FastAPI

from app.adapters.http.routers import system_router

app = FastAPI(
    title="HelpDesk Hub API",
    description="API de gestão de chamados para suporte técnico",
    version="1.0.0",
)

app.include_router(system_router.router)
