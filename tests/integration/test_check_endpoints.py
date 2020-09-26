from tests.integration.conftest import BaseTestControllers, get_authorization_string
from tests.integration.fake_mock_data import DBTestingData


class TestControllers(BaseTestControllers):
    def test_index_get(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_index_post_unregistered_user(self, client):
        response = client.post("/token", data={"username": "franco", "password": 1234},)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.text

    def test_index_post_registered_user_wrong_password(self, client):
        response = client.post(
            "/token", data={"username": DBTestingData.TEST_USER, "password": "...",},
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

    def test_sign_in_new_user_post(self, client, unit_of_work):
        # Unregistered user
        response = client.post(
            "/sign_in",
            json={"username": "new_user", "password": "1234", "password2": "1234"},
        )
        with unit_of_work as uow:
            user = uow.repository.get_username("new_user")
        assert response.status_code == 200
        assert user is not None
        assert user.username == "new_user"

    def test_sign_in_registered_user_post(self, client, unit_of_work):
        # Recent registered user
        response = client.post(
            "/sign_in",
            json={
                "username": DBTestingData.TEST_USER,
                "password": "1234",
                "password2": "1234",
            },
        )
        with unit_of_work as uow:
            user = uow.repository.get_username(DBTestingData.TEST_USER)
        assert response.status_code == 409
        assert user is not None
        assert user.username == DBTestingData.TEST_USER

    def test_api_search_books(self, client):
        username = DBTestingData.TEST_USER
        password = DBTestingData.TEST_PSW
        auth_str = get_authorization_string(client, username, password)
        response = client.get(
            "book/search",
            params={"search_params": "isbn", "value": "1234"},
            headers={"Authorization": auth_str},
        )
        print(response.json())
        assert response.status_code == 200

    def test_api_get_goodread_data(self, client):
        username = DBTestingData.TEST_USER
        password = DBTestingData.TEST_PSW
        auth_str = get_authorization_string(client, username, password)
        response = client.get("/book/10", headers={"Authorization": auth_str})
        assert response.status_code == 200

    def test_api_get_goodread_data_bad_password(self, client):
        response = client.get("/book/10", headers={"Authorization": "1234"})
        assert response.status_code == 401

    def test_api_insert_review_ok(self, client):
        username = DBTestingData.TEST_USER
        password = DBTestingData.TEST_PSW
        auth_str = get_authorization_string(client, username, password)
        response = client.post(
            "/book/10",
            json={"value": 5, "comment": "Good"},
            headers={"Authorization": auth_str},
        )
        print(response.json())
        assert response.status_code == 200
