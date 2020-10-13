from typing import Tuple
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.db.repositories.unit_of_work import UnitOfWork
from src.db.models.users import Users


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthenticationService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def login(self, username: str, password: str) -> Tuple[str, bool, Users]:
        with self.uow as uow:
            user = uow.repository.get_username(username)
        # Users.query.filter_by(username=username).first()
        if user is not None and user.validate_pass(password):
            return "Logged in successfully", True, user
        return "Username or password incorrect. Please try again", False, None

    def add_new_user(self, username: str, password: str):
        with self.uow as uow:
            user = uow.repository.get_username(username)
            if not user:
                user = dict(username=username, password=password)
                uow.repository.add_user(user)
                uow.commit()
                return 1
            return 0

    def signin(self, username: str, password: str, password2: str) -> Tuple[str, bool]:
        if password == password2:
            new_user_status = self.add_new_user(username, password)
            if new_user_status:
                return "User signed up", True
            return "Username already exists, pick up another.", False
        return "Passwords are not equal. Try again", False

    def create_access_token(self, username: str, password: str) -> Tuple[str, bool]:
        _, status, _ = self.login(username, password)
        if not status:
            return "", False
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + expires_delta
        to_encode = {"sub": username, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt, True

    def get_current_user(self, token: str) -> Tuple[bool, Users]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return False, None
        except JWTError:
            return False, None
        with self.uow:
            user = self.uow.repository.get_username(username)
        if user is None:
            return False, None
        return True, user
