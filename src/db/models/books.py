import numpy as np
from typing import Dict, List
from src.db.models.reviews import Reviews


class Books:
    def __init__(self, isbn, title, author, year, book_id=None):
        self.id = book_id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        # Relationships
        self.reviews: List[Reviews] = []
        # reviews = db.relationship("Reviews", backref="books", lazy=True)

    def _average_review(self) -> float:
        if self._get_review_count() == 0:
            return 0
        else:
            return np.array([r.review_value for r in self.reviews]).mean()

    def _get_review_count(self) -> int:
        return len(self.reviews)

    def user_can_insert_review(self, user_id: int):
        result = user_id in (r.user_id for r in self.reviews)
        return not result

    def as_dict(self) -> Dict:
        result = vars(self)
        result["reviews"] = self._average_review()
        return result
