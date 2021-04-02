from src.api.dependencies import get_db
from src.db import CRUDUserFactory
from tests.integration.conftest import BaseTestControllers, get_authorization_string
from tests.integration.fake_mock_data import DBTestingData


class TestEndpointLogIn(BaseTestControllers):
    def test_index_post_unregistered_user(self, client):
        response = client.post(
            "/token",
            data={"username": "franco", "password": 1234},
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.text

    def test_index_post_registered_user_wrong_password(self, client):
        response = client.post(
            "/token",
            data={"username": DBTestingData.TEST_USER, "password": "...",},
        )
        assert response.status_code == 401
        assert "Incorrect username or password" in response.text

    def test_index_post_registered_user(self, client):
        response = client.post(
            "/token",
            data={
                "username": DBTestingData.TEST_USER,
                "password": DBTestingData.TEST_PSW,
            },
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "token_type" in response.json()

    def test_sign_in_new_user_post(self, client):
        # Unregistered user
        response = client.post(
            "/sign_in",
            json={"username": "new_user", "password": "1234", "password2": "1234"},
        )
        crud_user = CRUDUserFactory(
            session_db=next(get_db())
        )
        user = crud_user.get_by_username(username="new_user")
        assert response.status_code == 200
        assert user is not None
        assert user.username == "new_user"

    def test_sign_in_registered_user_post(self, client):
        # Recent registered user
        response = client.post(
            "/sign_in",
            json={
                "username": DBTestingData.TEST_USER,
                "password": "1234",
                "password2": "1234",
            },
        )
        crud_user = CRUDUserFactory(
            session_db=next(get_db())
        )
        user = crud_user.get_by_username(username=DBTestingData.TEST_USER)
        assert response.status_code == 409
        assert user is not None
        assert user.username == DBTestingData.TEST_USER

