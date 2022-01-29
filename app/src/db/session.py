from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings
from logger import get_logger

logger = get_logger("db_session")

engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("Create session")
