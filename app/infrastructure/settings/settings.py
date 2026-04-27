from enum import StrEnum

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.infrastructure.logging.logger import getLogLevelNames


class AppEnv(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    project_title: str
    project_name: str
    project_description: str
    project_version: str

    environment: AppEnv = AppEnv.DEVELOPMENT
    port: int = 8000
    log_level: str = "INFO"

    database_url: str | None = None

    @field_validator("log_level", mode="before")
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
        return self.environment == AppEnv.DEVELOPMENT


settings = Settings()  # pyright: ignore[reportCallIssue]
