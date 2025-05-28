from db.mongo_client import MongoClient
from db.es import ElasticSearchClient
from db.redis_client import RedisClient
from db.session import SessionLocal

from config.db_config import ES_URL, ES_USERNAME, ES_PASSWORD, MONGO_URI

def get_redis_client():
    return RedisClient()

def get_mongo_client():
    """
    Create a MongoDB client.
    """
    mongo_client = MongoClient(MONGO_URI, database_name="movie_db")
    return mongo_client

def get_es_client():
    """
    Create an ElasticSearch client.
    """
    es_client = ElasticSearchClient(ES_URL, ES_USERNAME, ES_PASSWORD)
    return es_client

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