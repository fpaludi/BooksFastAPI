from src.db.models.review import Review
from typing import List, Tuple, Optional
from src.schemas.book import Book
from src.schemas.user import User
from src.schemas.review import ReviewCreate, Review
from src.db import CRUDBook, CRUDReview
from src.api.exceptions import BookAlreadyReviewed


class BookService:
    def __init__(
        self,
        crud_book: CRUDBook,
        crud_review: CRUDReview,
    ):
        self._crud_book = crud_book
        self._crud_review = crud_review

    def get_books_by(self, column_name: str, value: str) -> List[Book]:
        books = self._crud_book.get_by_column(column_name, value)
        return books

    def get_books_by_id(self, id_value: int) -> Optional[Book]:
        book = self._crud_book.get(id=id_value)
        return book

    def insert_book_review(
        self,
        book: Book,
        user: User,
        review_value: int,
        review_comment: str
    ) -> Optional[Review]:
        if not book.reviewed_by_user(user):
            new_review = ReviewCreate(
                review_value=review_value,
                review_comment=review_comment,
                user_id=user.id,
                book_id=book.id,
            )
            review = self._crud_review.create(obj_in=new_review)
        else:
            review = None
        return review
