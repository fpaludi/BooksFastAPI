import os
from os.path import dirname, join
from dotenv import load_dotenv
from fastapi import FastAPI

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

class Settings:  # i.e. Production
    DATABASE_URL = os.environ.get("DATABASE_URL")
    GOODREAD_API_KEY = os.environ.get("GOODREAD_API_KEY")
    GOODREAD_API_URL = os.environ.get("GOODREAD_API_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WTF_CSRF_ENABLED = True


class ProdSettings:
    pass


class DevSettings:
    DEBUG = True


class TestSettings:
    TESTING = True
    DATABASE_URL = os.environ.get("DATABASE_TEST_URL")
    WTF_CSRF_ENABLED = False


def update_settings(config_name="default"):
    global Settings
    config = {
        "development": DevSettings,
        "testing": TestSettings,
        "production": ProdSettings,
        "default": DevSettings,
    }
    for k in config[config_name].__dict__.keys():
        if not k.startswith("__"):
            setattr(Settings, k, config[config_name].__dict__[k])


def create_app(config_name="default"):
    from src.db.models import orm

    update_settings(config_name)
    app = FastAPI(title="BooksAPI",)

    from src.api.controllers import control
    app.include_router(control)

    # Start ORM Mappers
    orm.start_mappers()

    return app
