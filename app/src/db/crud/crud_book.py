from typing import Any, List
from sqlalchemy import inspect
from dependency_injector.providers import Factory
from src.db.crud.crud_base import CRUDBase
from src.db.models.book import Book as BookDbModel
from src.schemas.book import Book, BookCreate, BookUpdate


class CRUDBook(CRUDBase[BookDbModel, Book, BookCreate, BookUpdate]):
    def get_by_column(self, column_name: str, value: Any) -> List[Book]:
        insp = inspect(BookDbModel)
        books_db = (
            self.db.query(BookDbModel)
            .filter(insp.all_orm_descriptors[column_name].like(f"%{value}%"))
            .all()
        )
        books_schema = [self.schema.from_orm(book) for book in books_db]
        return books_schema


CRUDBookFactory = Factory(CRUDBook, model=BookDbModel, schema=Book)
