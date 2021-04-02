from typing import Generator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.db.session import SessionLocal
from src.services.factories import ServicesContainer
from src.schemas import User
from src.api.exceptions import CredentialException
from src.services import (
    BookService,
    GoodReadApiService,
    AuthenticationService,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    db = next(get_db())
    auth_service = ServicesContainer.auth_service_factory(
        crud_user__session_db=db
    )
    user = auth_service.get_current_user(token)
    if not user:
        raise CredentialException
    return user


def get_auth_service() -> AuthenticationService:
    db = next(get_db())
    auth_service = ServicesContainer.auth_service_factory(
        crud_user__session_db=db
    )
    return auth_service


def get_book_service() -> BookService:
    db = next(get_db())
    book_service = ServicesContainer.book_service_factory(
        crud_book__session_db=db,
        crud_review__session_db=db,
    )
    return book_service


def get_goodread_api_service() -> GoodReadApiService:
    goodread_service = ServicesContainer.goodread_service_factory()
    return goodread_service
