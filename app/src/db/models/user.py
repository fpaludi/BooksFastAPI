
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)
from src.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    confirmed = Column(Boolean, default=False)
    is_superuser = Column(Boolean(), default=False)
    password_hash = Column(String, nullable=False)
