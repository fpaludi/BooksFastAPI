from abc import ABC
from src.db.crud.crud_user import CRUDUser
import pytest
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from pydantic import PostgresDsn  # noqa
from app_factory import app_factory
from settings import settings
from src.schemas import user, book, review
from src.db import CRUDBookFactory, CRUDUserFactory, CRUDReviewFactory
from src.db import CRUDBook, CRUDUser, CRUDReview
from create_tables import create_tables, delete_tables
from tests.integration.fake_mock_data import DBTestingData


def pytest_configure():
    print("\nINITIAL Test configuration")
    print("Upload Setting object for testing pourposes")

    dotenv_path = ".test.env"
    test_env = dotenv_values(dotenv_path)
    TEST_POSTGRES_SERVER = test_env.get("POSTGRES_SERVER")
    TEST_POSTGRES_USER = test_env.get("POSTGRES_USER")
    TEST_POSTGRES_PASSWORD = test_env.get("POSTGRES_PASSWORD")
    TEST_POSTGRES_DB = test_env.get("POSTGRES_DB")
    TEST_DATABASE_URI = PostgresDsn.build(
        scheme="postgresql",
        user=TEST_POSTGRES_USER,
        password=TEST_POSTGRES_PASSWORD,
        host=TEST_POSTGRES_SERVER,
        path=f"/{TEST_POSTGRES_DB or ''}",
    )

    settings.DATABASE_URI = TEST_DATABASE_URI
    print(settings.DATABASE_URI)
    if settings.DATABASE_URI != TEST_DATABASE_URI:
        raise ValueError("Tests are not using testing database")
    settings.LOG_LEVEL = "DEBUG"
    settings.LOG_FILE = "test.log"


class BaseTestControllers(ABC):
    @pytest.fixture(scope="class")
    def client(self):
        # Create App Object
        app = app_factory()

        # Create DB for testing
        try:
            self.delete_testing_database()
        except Exception as exp:  # noqa
            print(exp)
        self.create_testing_database()

        # "Running"
        test_client = TestClient(app)
        try:
            yield test_client
        finally:
            # Clean testing DB to start clean every run tests
            self.delete_testing_database()

    def create_testing_database(self):
        engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

        if "_test" not in str(engine.url):
            print("Tests are running over production or development database")
            print(f"Database url: {engine.url}")
            raise (ValueError)

        print()
        print("*" * 80)
        print("TEST DB OPERATIONS")
        print("*" * 80)
        create_tables(engine, session)

        # Add User and Review
        crud_user = CRUDUserFactory(session_db=session)
        crud_book = CRUDBookFactory(session_db=session)
        crud_review = CRUDReviewFactory(session_db=session)

        new_user = user.UserCreate(
            username=DBTestingData.TEST_USER, password=DBTestingData.TEST_PSW,
        )
        user1 = crud_user.create(obj_in=new_user)
        book1 = crud_book.get_by_column("title", DBTestingData.BOOK_TITLE_W_REVIEW)[0]
        new_review = review.ReviewCreate(
            review_value="1",
            review_comment="test comment",
            user_id=user1.id,
            book_id=book1.id,
        )
        review1 = crud_review.create(obj_in=new_review)

        session.close()  # noqa
        engine.dispose()
        print("-" * 80)

    def delete_testing_database(self):
        engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

        print()
        print("*" * 80)
        print("TEST DB OPERATIONS")
        print("*" * 80)

        delete_tables(engine, session)
        session.close()  # noqa
        engine.dispose()
        print("-" * 80)

    # @classmethod
    # def setup_class(cls):
    #    # Create Env Variables and App
    #    CONF_NAME = "testing"
    #    app = create_app(CONF_NAME)
    #    # Create DB for testing
    #    create_tables()

    # @classmethod
    # def teardown_method(cls):
    #    # Clean testing DB to start clean every run tests
    #    delete_tables()


def get_authorization_string(client: TestClient, user: str, password: str):
    response = client.post(
        "/token", data={"username": user, "password": password},
    ).json()

    return f"{response['token_type']} {response['access_token']}"
