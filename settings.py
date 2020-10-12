from os.path import dirname, join
from dotenv import load_dotenv
from pydantic import BaseSettings
from dependency_injector import providers

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    DATABASE_URI: str
    GOODREAD_API_KEY: str
    GOODREAD_API_URL: str
    SECRET_KEY: str
    DEBUG: bool = False
    TESTING: bool = False


settings_factory = providers.Singleton(Settings)
settings = settings_factory()
