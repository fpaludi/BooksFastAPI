from typing import List, Tuple
from src.db.models.books import Books
from src.db.models.users import Users
from src.db.repositories.unit_of_work import UnitOfWork

# from src.models.reviews import Reviews


class BookServices:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_books_by(self, column_name: str, value: str) -> List[Books]:
        # books = Books.query.filter(
        #    Books.__table__.columns[column_name].like(f"%{value}%")
        # ).all()
        with self.uow as uow:
            books = uow.repository.get_book_by_like(column_name, value)
        return books

    def get_books_by_id(self, id_value: int) -> Books:
        # book = Books.query.get(id_value)
        with self.uow as uow:
            book = uow.repository.get_book_id(id_value)
        return book

    def insert_book_review(
        self, book: Books, user: Users, review_value: int, review_comment: str
    ) -> Tuple[str, bool]:
        if book.user_can_insert_review(user.id):
            new_review = dict(
                review_value=review_value,
                review_comment=review_comment,
                user_id=user.id,
                book_id=book.id,
            )
            with self.uow as uow:
                uow.repository.add_review(new_review)
                uow.commit()
            return "Review Inserted", True
        return "You have already inserted a review for this book", False
