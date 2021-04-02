import dependency_injector.containers as containers
import dependency_injector.providers as providers
from settings import settings
from src.db import (
    CRUDReviewFactory,
    CRUDUserFactory,
    CRUDBookFactory,
)
from src.core.security import JWTTokenizer
from src.services.book_service import BookService
from src.services.authentication_service import AuthenticationService
from src.services.external_api_service import GoodReadApiService


class ServicesContainer(containers.DeclarativeContainer):
    book_service_factory = providers.Factory(
        BookService, crud_book=CRUDBookFactory, crud_review=CRUDReviewFactory,
    )

    auth_service_factory = providers.Factory(
        AuthenticationService, tokenizer=JWTTokenizer(), crud_user=CRUDUserFactory,
    )

    goodread_service_factory = providers.Factory(
        GoodReadApiService, settings.GOODREAD_API_URL, settings.GOODREAD_API_KEY,
    )
