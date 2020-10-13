from typing import Optional, Dict, Any
from pydantic import BaseSettings, PostgresDsn, validator  # noqa
from dependency_injector import providers


class Settings(BaseSettings):
    GOODREAD_API_KEY: str
    GOODREAD_API_URL: str
    SECRET_KEY: str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DEBUG: Optional[bool] = False
    TESTING: Optional[bool] = False
    DATABASE_URI: Optional[PostgresDsn] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(  # noqa
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


settings_factory = providers.Singleton(Settings)
settings = settings_factory()
