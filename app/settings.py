from typing import Optional, Dict, Any
from pydantic import BaseSettings, PostgresDsn, validator, constr  # noqa
from dependency_injector import providers


class Settings(BaseSettings):
    # Goodread API
    GOODREAD_API_KEY: str
    GOODREAD_API_URL: str

    # DB
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[PostgresDsn] = None

    # Run Mode
    DEBUG: Optional[bool] = False
    TESTING: Optional[bool] = False

    # Security
    SECRET_KEY: constr(min_length=10)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # LOGGER
    LOG_LEVEL = "INFO"
    LOG_FILE = "app.log"

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


settings = Settings()
