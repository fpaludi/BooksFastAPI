from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.services.factories import ServicesContainer
from src.api.models import UserInDB
from src.api.exceptions import CredentialException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    auth_service = ServicesContainer.auth_service()
    status, user = auth_service.get_current_user(token)
    if not status:
        return CredentialException
    user_dict = {
        "username": user.username,
        "id": user.id,
        "password_hash": user.password_hash,
    }
    return UserInDB(**user_dict)
