from enum import Enum

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.infrastructure.logging.logger import getLogLevelNames


class AppEnv(Enum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_title: str
    app_name: str
    app_description: str
    app_version: str
    app_env: AppEnv = AppEnv.DEVELOPMENT
    app_port: int = 8000
    app_log_level: str = "INFO"

    @field_validator("app_log_level", mode="before")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        valid_levels = getLogLevelNames()
        if value not in valid_levels:
            raise ValueError(
                f"Invalid log level: {value}. "
                f"Expected one of: {', '.join(valid_levels.keys())}"
            )
        return value

    @property
    def is_development(self) -> bool:
        return self.app_env == AppEnv.DEVELOPMENT


settings = Settings()  # pyright: ignore[reportCallIssue]
