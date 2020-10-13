import pytest
from dotenv import dotenv_values
from fastapi.testclient import TestClient
from pydantic import PostgresDsn  # noqa
from abc import ABC
from app_factory import app_factory
from settings import settings
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


class BaseTestControllers(ABC):
    @pytest.fixture(scope="class")
    def client(self):
        # Create App Object
        app = app_factory()

        # Create DB for testing
        try:
            self.delete_testing_database()
        except:  # noqa
            pass
        self.create_testing_database()

        # "Running"
        test_client = TestClient(app)
        try:
            yield test_client
        finally:
            # Clean testing DB to start clean every run tests
            self.delete_testing_database()

    @pytest.fixture(scope="function")
    def unit_of_work(self):
        from src.db.repositories.factories import RepositoryContainer

        uow = RepositoryContainer.uow()
        return uow

    def create_testing_database(self):
        from src.db.repositories.factories import RepositoryContainer

        engine = RepositoryContainer.engine()
        session = RepositoryContainer.DEFAULT_SESSIONFACTORY()
        if "_test" not in str(engine.url):
            print("Tests are running over production or development database")
            print(f"Database url: {engine.url}")
            raise (ValueError)

        print()
        print("*" * 80)
        print("TEST DB OPERATIONS")
        print("*" * 80)
        create_tables(engine, session)
        uow = RepositoryContainer.uow()

        # Add User
        with uow:
            new_user = dict(
                username=DBTestingData.TEST_USER, password=DBTestingData.TEST_PSW
            )
            uow.repository.add_user(new_user)
            uow.commit()

            # Add Review for User
            user = uow.repository.get_username(DBTestingData.TEST_USER)
            book = uow.repository.get_book_by_like(
                "title", DBTestingData.BOOK_TITLE_W_REVIEW
            )[0]
            new_review = dict(
                review_value="1",
                review_comment="test comment",
                user_id=user.id,
                book_id=book.id,
            )
            uow.repository.add_review(new_review)
            uow.commit()
        print("-" * 80)

    def delete_testing_database(self):
        from src.db.repositories.factories import RepositoryContainer

        print()
        print("*" * 80)
        print("TEST DB OPERATIONS")
        print("*" * 80)
        engine = RepositoryContainer.engine()
        session = RepositoryContainer.DEFAULT_SESSIONFACTORY()
        delete_tables(engine, session)
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
