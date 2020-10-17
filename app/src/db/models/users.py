from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Users:
    def __init__(self, username, password, user_id=None):
        self.id = user_id
        self.username = username
        self.password = password
        self.confirmed = True

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = pwd_context.hash(password)

    def validate_pass(self, password):
        return pwd_context.verify(password, self.password_hash)
