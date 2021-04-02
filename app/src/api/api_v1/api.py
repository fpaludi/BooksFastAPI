from fastapi import APIRouter

from src.api.api_v1.endpoints import books, login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
