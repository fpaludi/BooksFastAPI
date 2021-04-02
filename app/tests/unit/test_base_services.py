import pytest
import mock
from abc import ABC
from sqlalchemy.orm import sessionmaker, Session
from src.services import  (
    BookService,
    GoodReadApiService,
    AuthenticationService,
)
from src.db import (
    CRUDBook,
    CRUDUser,
    CRUDReview,
)
from src.schemas import user, review, user
from src.core.security import Tokenizer

class BaseTestService(ABC):
    def teardown_method(self):
        pass

    @pytest.fixture(scope="function")
    def crud_user_mock(self) -> CRUDUser:
        return mock.create_autospec(CRUDUser)

    @pytest.fixture(scope="function")
    def crud_book_mock(self) -> CRUDBook:
        return mock.create_autospec(CRUDBook)

    @pytest.fixture(scope="function")
    def crud_review_mock(self) -> CRUDReview:
        return mock.create_autospec(CRUDReview)

    @pytest.fixture(scope="function")
    def tokenizer_mock(self) -> Tokenizer:
        return mock.create_autospec(Tokenizer)

    @pytest.fixture(scope="function")
    def book_service(
        self,
        crud_book_mock: CRUDBook,
        crud_review_mock: CRUDReview
    ):
        # Service
        book_service = BookService(
            crud_book=crud_book_mock,
            crud_review=crud_review_mock,
        )

        # lambdas
        book_service.get_crud_book_mock = lambda: crud_book_mock
        book_service.get_crud_review_mock = lambda: crud_review_mock

        return book_service

    @pytest.fixture(scope="function")
    def authentication_service(
        self,
        crud_user_mock: CRUDUser,
        tokenizer_mock: Tokenizer,
    ):
        # Service
        authentication_service = AuthenticationService(
            crud_user=crud_user_mock,
            tokenizer=tokenizer_mock
        )

        # Lambdas
        authentication_service.get_crud_user_mock = lambda: crud_user_mock
        authentication_service.get_tokenizer_mock = lambda: tokenizer_mock

        return authentication_service

    @pytest.fixture(scope="function")
    def goodread_api_service(self):
        # Service
        external_api_service = GoodReadApiService("URL", "KEY")

        return external_api_service
