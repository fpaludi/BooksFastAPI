from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)
from src.db.base_class import Base


class Review(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)  # noqa
    review_value = Column(Integer, nullable=False)
    review_comment = Column(Text)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
