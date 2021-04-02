from src.api.dependencies import get_db
from src.db import CRUDUserFactory
from tests.integration.conftest import BaseTestControllers, get_authorization_string
from tests.integration.fake_mock_data import DBTestingData


class TestEndpointBooks(BaseTestControllers):

    def test_api_search_books(self, client):
        username = DBTestingData.TEST_USER
        password = DBTestingData.TEST_PSW
        auth_str = get_authorization_string(client, username, password)
        response = client.get(
            "books/search",
            params={"search_params": "isbn", "value": "1234"},
            headers={"Authorization": auth_str},
        )
        assert response.status_code == 200

    def test_api_insert_review_ok(self, client):
        username = DBTestingData.TEST_USER
        password = DBTestingData.TEST_PSW
        auth_str = get_authorization_string(client, username, password)
        response = client.post(
            "/books/10",
            json={"review_value": 5, "review_comment": "Good"},
            headers={"Authorization": auth_str},
        )
        assert response.status_code == 200

    def test_api_insert_review_bad_auth(self, client):
        response = client.post(
            "/books/10",
            json={"review_value": 5, "review_comment": "Good"},
            headers={"Authorization": "Messi"},
        )
        assert response.status_code == 401

    def test_api_insert_review_not_existing_book(self, client):
        username = DBTestingData.TEST_USER
        password = DBTestingData.TEST_PSW
        auth_str = get_authorization_string(client, username, password)
        response = client.post(
            "/books/9999999999999999999999999999",
            json={"review_value": 5, "review_comment": "Good"},
            headers={"Authorization": auth_str},
        )
        assert response.status_code == 404

    def test_api_show_book(self, client):
        username = DBTestingData.TEST_USER
        password = DBTestingData.TEST_PSW
        auth_str = get_authorization_string(client, username, password)
        response = client.get(
            "/books/1",
            headers={"Authorization": auth_str},
        )
        assert response.status_code == 200
        assert response.json()["isbn"] == "0380795272"
