from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnv(Enum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_env: AppEnv = AppEnv.DEVELOPMENT
    app_port: int = 8000

    @property
    def is_development(self) -> bool:
        return self.app_env == AppEnv.DEVELOPMENT


settings = Settings()
