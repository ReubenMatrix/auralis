from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from app.core.config import settings
from app.core.logger import logger


try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size = 10,
        max_overflow = 20,
    )
    logger.info("Postgres initialized")
except Exception as e:
    logger.critical(f"Failed to initialize Database connection engine : {e}")
    raise

SessionLocal =sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()


def init_db() -> Session:
    db = None

    try:
        db = SessionLocal()
        yield db

    except SQLAlchemyError as e:
        logger.error(f"DB Session error: {e}")
        raise

    finally:
        if db:
            db.close()
            logger.debug("DB Session Closed")


@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = engine.connect()
        logger.debug("DB Connection Established")
        yield conn
    
    except SQLAlchemyError as e:
        logger.error(f"DB Connection Error: {e}")
        raise

    finally:
        if conn:
            conn.close()
            logger.debug("DB Connection Closed")
    