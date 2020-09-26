from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field  # pylint: disable=E0611


class BookSearchOptions(str, Enum):
    isbn = "isbn"
    author = "author"
    title = "title"


class SearchBook(BaseModel):
    reference: BookSearchOptions
    value: str


class BookReview(BaseModel):
    value: int = Field(ge=0, le=5)
    comment: Optional[str]


class Book(BaseModel):
    isbn: str
    title: str
    author: str
    year: int
    reviews: Optional[float] = None


class UserBase(BaseModel):
    username: str


class UserSignIn(UserBase):
    password: str
    password2: str


class UserInDB(UserBase):
    id: int  # noqa
    password_hash: str


class Token(BaseModel):
    access_token: str
    token_type: str
