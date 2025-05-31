from db.mongo_client import MongoClient
from db.es import ElasticSearchClient
from db.redis_client import RedisClient
from db.session import SessionLocal
from db.chroma import ChromaDBClient

from config.db_config import ES_URL, ES_USERNAME, ES_PASSWORD, MONGO_URI, REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

def get_redis_client():
    return RedisClient(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)

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

def get_chroma_client():
    """
    Create a ChromaDB client.
    """
    chroma_client = ChromaDBClient()
    return chroma_client