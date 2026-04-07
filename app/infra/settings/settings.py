from enum import Enum

from pydantic_settings import BaseSettings


class AppEnv(Enum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):
    app_env: AppEnv = AppEnv.DEVELOPMENT

    class Config:
        env_file: str = ".env"


settings = Settings()
