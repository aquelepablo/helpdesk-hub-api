from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"

    class Config:
        env_file: str = ".env"


settings = Settings()
