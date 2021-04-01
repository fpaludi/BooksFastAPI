from fastapi import FastAPI
from settings import settings  # noqa


def app_factory():
    app = FastAPI(title="BooksAPI",)
    from src.api.api_v1.api import api_router

    app.include_router(api_router)
    return app
