import uvicorn

from app.infrastructure.settings.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=settings.app_port,
        reload=settings.is_development,
    )
