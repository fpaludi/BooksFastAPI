from fastapi import FastAPI
from settings import settings  # noqa


def app_factory():
    from src.db.models import orm

    app = FastAPI(title="BooksAPI",)

    from src.api.controllers import control

    app.include_router(control)

    # Start ORM Mappers
    orm.start_mappers()

    return app
