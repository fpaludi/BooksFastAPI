from typing import Optional, List
from pydantic import BaseModel, Field
from src.schemas.review import Review
from src.schemas.user import User

# Shared properties
class BookBase(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[str] = None
    reviews: List[Review] = Field(default_factory=list)


# Properties to receive on Book creation
class BookCreate(BookBase):
    isbn: str
    title: str
    author: str
    year: str


# Properties to receive on Book update
class BookUpdate(BookBase):
    pass


# Properties shared by models stored in DB
class BookInDBBase(BookBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Book(BookInDBBase):

    def reviewed_by_user(self, user: User) -> bool:
        reviewers = [
            review.user_id for review in self.reviews
        ]
        return user.id in reviewers

# Additional properties stored in DB
class BookInDB(BookInDBBase):
    pass
