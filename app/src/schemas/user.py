from typing import Optional
from pydantic import BaseModel
from src.core import security


# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    confirmed: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    username: str
    password: str


class UserCreateForm(BaseModel):
    username: str
    password: str
    password2: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    password_hash: Optional[str] = None

    def verify_password(self, password: str):
        return security.verify_password(password, self.password_hash)


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password_hash: str

    #def validate_pass(self, password):
    #    return pwd_context.verify(password, self.password_hash)

