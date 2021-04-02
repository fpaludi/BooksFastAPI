from copy import deepcopy
from src.core.security import get_password_hash
from tests.unit.test_base_services import BaseTestService
from tests.unit import mock_io_data


class TestAuthenticationService(BaseTestService):
    def test_login_ok(self, authentication_service):
        # Load IO

        # Mock internal service
        test_user = deepcopy(mock_io_data.user1)
        test_user.password_hash = get_password_hash("1234")
        crud_user = authentication_service.get_crud_user_mock()
        crud_user.get_by_username.return_value = test_user

        # Method under test
        response = authentication_service.login("franco", "1234")

        # Assertions
        assert response == test_user

    def test_login_fail(self, authentication_service):
        # Load IO

        # Mock internal service
        crud_user = authentication_service.get_crud_user_mock()
        crud_user.get_by_username.return_value = mock_io_data.user1

        # Method under test
        response = authentication_service.login("franco", "12345")

        # Assertions
        assert response == None

    def test_signin_ok(self, authentication_service):
        # Load IO

        # Mock internal service
        crud_user = authentication_service.get_crud_user_mock()
        crud_user.create.return_value = mock_io_data.user1
        crud_user.get_by_username.return_value = None

        # Method under test
        response = authentication_service.sign_in("franco", "1234", "1234")

        # Assertions
        assert response == mock_io_data.user1

    def test_sign_in_fail(self, authentication_service):
        # Load IO

        # Mock internal service
        crud_user = authentication_service.get_crud_user_mock()
        crud_user.create.return_value = mock_io_data.user1
        crud_user.get_by_username.return_value = mock_io_data.user1

        # Method under test
        response = authentication_service.sign_in("franco", "1234", "1234")

        # Assertions
        assert response == None

    def test_sign_in_not_equal_passwords(self, authentication_service):
        # Load IO

        # Mock internal service
        crud_user = authentication_service.get_crud_user_mock()
        crud_user.get_by_username.return_value = mock_io_data.user1

        # Method under test
        response = authentication_service.sign_in("franco", "1234", "12345")

        # Assertions
        assert response == None
