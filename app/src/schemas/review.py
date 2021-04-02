from typing import Optional
from pydantic import BaseModel


# Shared properties
class ReviewBase(BaseModel):
    review_value: Optional[int] = None
    review_comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    review_value: int
    review_comment: str
    user_id: int
    book_id: int


class ReviewCreateForm(ReviewBase):
    review_value: int
    review_comment: str


# Properties to receive via API on update
class ReviewUpdate(ReviewCreate):
    pass


class ReviewInDBBase(ReviewBase):
    id: Optional[int] = None
    user_id: Optional[int] = None
    book_id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Review(ReviewInDBBase):
    pass


# Additional properties stored in DB
class ReviewInDB(ReviewInDBBase):
    user_id: int
    book_id: int
