from typing import Optional
from datetime import datetime, timedelta
from src.schemas import User, UserCreate, UserUpdate, user
from src.db import CRUDUser
from src.core.security import Tokenizer


class AuthenticationService:
    def __init__(
        self,
        crud_user: CRUDUser,
        tokenizer: Tokenizer
    ):
        self._crud_user = crud_user
        self._tokenizer = tokenizer

    def login(self, username: str, password: str) -> Optional[User]:
        user = self._crud_user.get_by_username(username=username)
        if user and user.verify_password(password):
            return user
        return None

    def add_new_user(self, username: str, password: str) -> User:
        new_user = UserCreate(username=username, password=password)
        return self._crud_user.create(obj_in=new_user)

    def sign_in(self, username: str, password: str, password2: str) -> Optional[User]:
        if password == password2:
            new_user = self.add_new_user(username, password)
            return new_user
        return None

    def create_access_token(self, username: str, password: str) -> Optional[str]:
        user = self.login(username, password)
        if not user:
            None
        return self._tokenizer.create_access_token(user.username)

    def get_current_user(self, token: str) -> Optional[User]:
        username = self._tokenizer.decode_access_token(token)
        user = None
        if username:
            user = self._crud_user.get_by_username(
                username=username,
            )
        return user
