import dependency_injector.containers as containers
import dependency_injector.providers as providers
from settings import settings
from src.db.repositories.factories import RepositoryContainer
from src.services.book_service import BookServices
from src.services.authentication_service import AuthenticationService
from src.services.external_api_service import ExternalApiService


class ServicesContainer(containers.DeclarativeContainer):
    book_service = providers.Factory(BookServices, RepositoryContainer.uow)
    auth_service = providers.Factory(AuthenticationService, RepositoryContainer.uow)

    api_service = providers.Factory(
        ExternalApiService, settings.GOODREAD_API_URL, settings.GOODREAD_API_KEY
    )
