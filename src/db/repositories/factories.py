import dependency_injector.providers as providers
import dependency_injector.containers as containers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings
from src.db.repositories.unit_of_work import UnitOfWork
from src.db.repositories.repository import Repository


class RepositoryContainer(containers.DeclarativeContainer):
    engine = providers.Singleton(create_engine, settings.DATABASE_URI)
    DEFAULT_SESSIONFACTORY = sessionmaker(bind=engine())
    repository_factory = providers.Factory(Repository)
    uow = providers.Factory(UnitOfWork, DEFAULT_SESSIONFACTORY, repository_factory)
