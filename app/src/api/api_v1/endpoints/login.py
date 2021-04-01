from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.services import AuthenticationService
from src.services.logger import get_logger
from src.schemas.auth import Token
from src.schemas import user
from src.api.dependencies import get_current_user, get_auth_service
from src.api.exceptions import (
    UserPassException,
    UserExistsException,
    DataNotFoundException,
)


# Global Objects
router = APIRouter()
logger = get_logger(__name__)


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    access_token = auth_service.create_access_token(
        form_data.username, form_data.password
    )
    if not access_token:
        raise UserPassException
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/sign_in", response_model=user.UserBase)
def sign_in(
    user: user.UserCreateForm,
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    user = auth_service.sign_in(**user.dict())
    if not user:
        raise UserExistsException
    logger.info(f"user {user.username} signed in")
    return user


@router.get("/logout")
def logout():
    logger.info("logging out")
