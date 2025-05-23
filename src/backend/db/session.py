from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config.db_config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# Example: mysql+pymysql://user:password@host:port/dbname
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model to inherit from
Base = declarative_base()

def get_db():
    """
    Dependency to get the database session.

    Yields:
        Session: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()