from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.api.models import BookSearchOptions, BookReview, Token, UserSignIn
from src.api.exceptions import (
    CredentialException,
    UserPassException,
    UserExistsException,
    DataNotFoundException,
)
from src.api.models import UserInDB, Book
from src.services import ServicesContainer
from src.services.logger import LoggerBuilder

# Global Objects
control = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logger = LoggerBuilder(__name__).get_logger()


def get_current_user(token: str = Depends(oauth2_scheme)):
    auth_service = ServicesContainer.auth_service()
    status, user = auth_service.get_current_user(token)
    if not status:
        return CredentialException
    user_dict = {
        "username": user.username,
        "id": user.id,
        "password_hash": user.password_hash,
    }
    return UserInDB(**user_dict)


@control.get("/",)
def index():
    logger.info("index")
    return {"message": "welcome!"}


@control.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_service = ServicesContainer.auth_service()
    access_token, status = auth_service.create_access_token(
        form_data.username, form_data.password
    )
    if not status:
        raise UserPassException
    return {"access_token": access_token, "token_type": "bearer"}


@control.post("/sign_in")
def sign_in(user: UserSignIn):
    logger.info(f"user {user.username} signing in")
    auth_service = ServicesContainer.auth_service()
    msg, status = auth_service.signin(**user.dict())
    if not status:
        raise UserExistsException
    return {"message": msg}


@control.get("/logout")
def logout():
    logger.info("logging out")
    return {"message": "logout"}


@control.get("/book/search")
def search_book(
    search_params: BookSearchOptions,
    value: str,
    curret_user: UserInDB = Depends(get_current_user),
):
    logger.info(f"user {curret_user.username} looking for books")
    book_service = ServicesContainer.book_service()
    return {"books": book_service.get_books_by(search_params, value)}


@control.get("/book/{book_id}", response_model=Book)
def show_book(book_id: int, curret_user: UserInDB = Depends(get_current_user)):
    logger.info(f"user {curret_user.username} looks book {book_id}")
    book_service = ServicesContainer.book_service()
    book = book_service.get_books_by_id(book_id)
    if book is None:
        raise DataNotFoundException
    book_dict = book.as_dict()
    return book_dict


@control.post("/book/{book_id}", response_model=Book)
def insert_book_review(
    book_id: int, review: BookReview, curret_user: UserInDB = Depends(get_current_user)
):
    logger.info(f"user {curret_user.username} review book {book_id}")
    book_service = ServicesContainer.book_service()
    book_to_rev = book_service.get_books_by_id(book_id)
    _, status = book_service.insert_book_review(
        book_to_rev, curret_user, review.value, review.comment
    )
    if status is None:
        raise DataNotFoundException
    book = book_service.get_books_by_id(book_id)
    book_dict = book.as_dict()
    return book_dict
