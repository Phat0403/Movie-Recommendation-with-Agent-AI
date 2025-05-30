DB_USER = "root"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "movie_recommendation"

MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_USERNAME = "root"
MONGO_PASSWORD = "example"
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"

MONGO_DB_NAME = "movie_db"

ES_SCHEMA = "http"
ES_HOST = "localhost"
ES_PORT = "9200"
ES_USERNAME = "elastic"
ES_PASSWORD = "changeme"
ES_URL = f"{ES_SCHEMA}://{ES_HOST}:{ES_PORT}"

CHROMA_DB_PATH = "chroma/" 
