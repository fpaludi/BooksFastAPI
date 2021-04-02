from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from src.db.base_class import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)  # noqa
    isbn = Column(String, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    reviews = relationship("Review", backref="book", collection_class=list, lazy=False)
