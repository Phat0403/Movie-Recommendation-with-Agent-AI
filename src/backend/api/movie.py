from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse

from db.mongo_client import MongoClient
from db.es import ElasticSearchClient
from db.redis_client import RedisClient
from db.clients import get_mongo_client, get_es_client, get_redis_client

from services.movie import MovieService
from schemas.movie import MovieList, MovieWithRatingList, MovieInESList, MovieDetails

import logging



def get_movie_service(mongo_client: MongoClient = Depends(get_mongo_client), es_client: ElasticSearchClient = Depends(get_es_client), redis_client: RedisClient = Depends(get_redis_client)):
    """
    Create a MovieService instance.
    """
    return MovieService(mongo_client=mongo_client, es_client=es_client, redis_client=redis_client)

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
        logging.error(f"Error fetching movies: {e}")
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
    
@router.get("/movies/trending", response_model=MovieWithRatingList)
async def get_movie_by_trending(movie_service: MovieService = Depends(get_movie_service), page: int = 0, offset: int = 20):
    """
    Get movies sorted by ratings.
    """
    try:
        movies = await movie_service.get_movies_by_trending(page=page, offset=offset)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching movies by ratings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/movies/numVote", response_model=MovieWithRatingList)
async def get_movie_by_numVotes(movie_service: MovieService = Depends(get_movie_service), page: int = 0, offset: int = 20):
    """
    Get movies sorted by ratings.
    """
    try:
        movies = await movie_service.get_movies_by_numVote(page=page, offset=offset)
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

@router.get("/movies/search/by-director", response_model=MovieInESList)
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

@router.get("/showtimes")
async def get_showtimes(movie_service: MovieService = Depends(get_movie_service)):
    """
    Get showtimes for movies.
    """
    try:
        showtimes = await movie_service.get_cinestar_showtimes()
        return JSONResponse(content=showtimes, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching showtimes: {e}")
        raise HTTPException(status_code=500, detail=str(e))