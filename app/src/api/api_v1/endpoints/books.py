from enum import Enum
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.services import BookService
from src.services.logger import get_logger
from src.schemas.auth import Token
from src.schemas import book, user, review
from src.api.dependencies import get_current_user, get_book_service
from src.api.exceptions import (
    DataNotFoundException,
)


# Global Objects
router = APIRouter()
logger = get_logger(__name__)


class BookSearchOptions(str, Enum):
    isbn = "isbn"
    author = "author"
    title = "title"


@router.get("/search")
def search_book(
    search_params: BookSearchOptions,
    value: str,
    curret_user: user.User = Depends(get_current_user),
    book_service: BookService = Depends(get_book_service),
):
    logger.info(f"user {curret_user.username} looking for books")
    return {"books": book_service.get_books_by(search_params, value)}


@router.get("/{book_id}", response_model=book.Book)
def show_book(
    book_id: int,
    curret_user: user.User = Depends(get_current_user),
    book_service: BookService = Depends(get_book_service),
):
    logger.info(f"user {curret_user.username} looks book {book_id}")
    book = book_service.get_books_by_id(book_id)
    if book is None:
        raise DataNotFoundException
    return book.dict()


@router.post("/{book_id}", response_model=book.Book)
def insert_book_review(
    book_id: int,
    review: review.ReviewCreateForm,
    curret_user: user.User = Depends(get_current_user),
    book_service: BookService = Depends(get_book_service),
):
    logger.info(f"user {curret_user.username} review book {book_id}")
    book_to_rev = book_service.get_books_by_id(book_id)
    if book_to_rev:
        book = book_service.insert_book_review(
            book=book_to_rev,
            user=curret_user,
            review_value=review.review_value,
            review_comment=review.review_comment
        )

    else:
        raise DataNotFoundException

    return book.dict()
