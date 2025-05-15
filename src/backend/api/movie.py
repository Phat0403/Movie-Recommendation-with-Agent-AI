from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse

from config.db_config import ES_URL, ES_USERNAME, ES_PASSWORD, MONGO_URI
from db.mongo_client import MongoClient
from db.es import ElasticSearchClient
from services.movie import MovieService
from schemas.movie import MovieList, MovieWithRatingList, MovieInESList, MovieDetails

import logging

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

def get_movie_service(mongo_client: MongoClient = Depends(get_mongo_client), es_client: ElasticSearchClient = Depends(get_es_client)):
    """
    Create a MovieService instance.
    """
    return MovieService(mongo_client, es_client)

router = APIRouter()

@router.get("/movies", response_model=MovieList)
async def get_movies(movie_service: MovieService = Depends(get_movie_service), page: int = 0, offset: int = 20):
    """
    Get a list of movies with pagination.
    """
    try:
        movies = await movie_service.get_movies(page=page, offset=offset)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/movie/{movie_id}", response_model=MovieDetails)
async def get_movie_description(movie_id: str, movie_service: MovieService = Depends(get_movie_service)):
    """
    Get a movie description by its ID.
    """
    try:
        movie_description = await movie_service.get_movie_description_by_tconst(movie_id)
        if not movie_description:
            raise HTTPException(status_code=404, detail="Movie not found")
        return JSONResponse(content=movie_description, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching movie description: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/movies/ratings", response_model=MovieWithRatingList)
async def get_movie_by_ratings(movie_service: MovieService = Depends(get_movie_service), page: int = 0, offset: int = 20):
    """
    Get movies sorted by ratings.
    """
    try:
        movies = await movie_service.get_movies_by_ratings(page=page, offset=offset)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching movies by ratings: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/movies/by-genre", response_model=MovieList)
async def get_movie_by_genre(genre: str, movie_service: MovieService = Depends(get_movie_service), page: int = 0, offset: int = 20):
    """
    Get movies sorted by genre.
    """
    try:
        movies = await movie_service.get_movies_by_genre(genre=genre, page=page, offset=offset)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching movies by genre: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/movies/by/{nconst}", response_model=MovieList)
async def get_movies_by_nconst(nconst: str, movie_service: MovieService = Depends(get_movie_service)):
    """
    Get movies by actor/actress ID (nconst).
    """
    try:
        movies = await movie_service.get_movies_by_nconst(nconst=nconst)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching movies by nconst: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/movies/search/by-title", response_model=MovieInESList)
async def search_movies(title: str, movie_service: MovieService = Depends(get_movie_service)):
    """
    Search for movies by title.
    """
    try:
        movies = await movie_service.search_movie_by_name(title)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error searching movies by title: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/movies/search_by_director", response_model=MovieInESList)
async def search_movies_by_director(director: str, movie_service: MovieService = Depends(get_movie_service)):
    """
    Search for movies by director.
    """
    try:
        movies = await movie_service.search_movie_by_director(director)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error searching movies by director: {e}")
        raise HTTPException(status_code=500, detail=str(e))