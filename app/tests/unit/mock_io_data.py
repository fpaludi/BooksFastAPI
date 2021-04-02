from src.schemas import book
from src.schemas import review
from src.schemas import user


user1 = user.User(username="franco", password="1234")
user1.id = 1
user2 = user.User(username="laura", password="pass")
user2.id = 2

book1 = book.Book(
    id=1, isbn="HP1", title="Harry Potter 1", author="J.K. Rowling", year=1999
)
book2 = book.Book(
    id=2, isbn="HP2", title="Harry Potter 2", author="J.K. Rowling", year=2001
)

review1 = review.Review(
    review_value=5, review_comment="Excelente", user_id=1, book_id=1
)
review2 = review.Review(review_value=5, review_comment="Magico", user_id=2, book_id=1)

book1.reviews = [review1, review2]
