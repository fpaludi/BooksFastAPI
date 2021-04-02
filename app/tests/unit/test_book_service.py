from src.schemas import book, review
from tests.unit.test_base_services import BaseTestService
from tests.unit import mock_io_data


class TestBookService(BaseTestService):
    def test_get_books_by_id(self, book_service):
        # Load IO

        # Mock internal service
        mock_result = mock_io_data.book2
        crud_book = book_service.get_crud_book_mock()
        crud_book.get.return_value = mock_result

        # Method under test
        response = book_service.get_books_by_id(2)

        # Assertions
        assert response == mock_result

    def test_get_books_by_id_no_exists(self, book_service):
        # Load IO

        # Mock internal service
        mock_result = None
        crud_book = book_service.get_crud_book_mock()
        crud_book.get.return_value = mock_result

        # Method under test
        response = book_service.get_books_by_id(1234)

        # Assertions
        assert response == mock_result

    def test_get_books_by(self, book_service):
        # Load IO

        # Mock internal service
        mock_result = [mock_io_data.book2]
        crud_book = book_service.get_crud_book_mock()
        crud_book.get_by_column.return_value = mock_result

        # Method under test
        response = book_service.get_books_by("title", "Harry Potter")

        # Assertions
        assert response == mock_result

    def test_get_books_by_no_exists(self, book_service):
        # Load IO

        # Mock internal service
        mock_result = []
        crud_book = book_service.get_crud_book_mock()
        crud_book.get_by_column.return_value = mock_result

        # Method under test
        response = book_service.get_books_by("title", "Harry Potter")

        # Assertions
        assert response == mock_result

    def test_insert_book_review_ok(self, book_service):
        # Load IO
        user = mock_io_data.user1
        book = mock_io_data.book2  # book has none reviews
        expected = review.Review(
            review_value=5,
            review_comment="Nice book",
            user_id=user.id,
            book_id=book.id,
        )

        # Mock internal service
        crud_review = book_service.get_crud_review_mock()
        crud_review.create.return_value = expected

        # Method under test
        response = book_service.insert_book_review(
            book,
            user,
            expected.review_value,
            expected.review_comment
        )

        # Assertions
        assert response == expected

    def test_insert_book_review_fail(self, book_service):
        # Load IO
        user = mock_io_data.user1
        book = mock_io_data.book1  # book has reviews form users 1 and 2

        # Method under test
        response = book_service.insert_book_review(
            book,
            user,
            4,
            "Good book",
        )

        # Assertions
        assert response == None
