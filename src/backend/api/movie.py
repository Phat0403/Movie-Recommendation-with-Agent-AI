from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from db.mongo_client import MongoClient
from db.es import ElasticSearchClient
from db.redis_client import RedisClient
from db.chroma import ChromaDBClient
from db.clients import get_mongo_client, get_es_client, get_redis_client, get_chroma_client

from services.movie import MovieService
from schemas.movie import MovieList, MovieInESList, MovieDetails

import logging

# Initialize the MovieService instance
mongo_client: MongoClient = get_mongo_client()
es_client: ElasticSearchClient = get_es_client()
redis_client: RedisClient = get_redis_client()
chroma_client: ChromaDBClient = get_chroma_client()

movie_service = MovieService(mongo_client=mongo_client, es_client=es_client, redis_client=redis_client, chroma_client=chroma_client)

router = APIRouter()

@router.get("/movies/explore", response_model=MovieList)
async def get_all_movies(year: int = 0, genre: str = "", sort: int = 0, page: int = 0, offset: int = 20):
    """
    Get a list of movies with pagination.
    """
    if genre == "all":
        genre = ""
    try:
        movies = await movie_service.get_all_movies(year=year, genre=genre, sort=sort, page=page, offset=offset)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching movies: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/movies", response_model=MovieList)
async def get_movies(page: int = 0, offset: int = 20):
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
async def get_movie_description(movie_id: str):
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

@router.get("/movies/ratings", response_model=MovieList)
async def get_movie_by_ratings(page: int = 0, offset: int = 20):
    """
    Get movies sorted by ratings.
    """
    try:
        movies = await movie_service.get_movies_by_ratings(page=page, offset=offset)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching movies by ratings: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/movies/trending", response_model=MovieList)
async def get_movie_by_trending(page: int = 0, offset: int = 20):
    """
    Get movies sorted by trending.
    """
    try:
        movies = await movie_service.get_movies_by_trending(page=page, offset=offset)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching trending movies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/movies/numVote", response_model=MovieList)
async def get_movie_by_numVotes(page: int = 0, offset: int = 20):
    """
    Get movies sorted by number of votes.
    """
    try:
        movies = await movie_service.get_movies_by_numVote(page=page, offset=offset)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching movies by numVotes: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/movies/by-genre", response_model=MovieList)
async def get_movie_by_genre(genre: str, page: int = 0, offset: int = 20):
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
async def get_movies_by_nconst(nconst: str):
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
async def search_movies(title: str):
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
async def search_movies_by_director(director: str):
    """
    Search for movies by director.
    """
    try:
        movies = await movie_service.search_movie_by_director(director)
        return JSONResponse(content=movies, status_code=200)
    except Exception as e:
        logging.error(f"Error searching movies by director: {e}")
        raise HTTPException(status_code=500, detail=str(e))


    
@router.get("/movies/recommend/{movie_id}", response_model=MovieList)
async def recommend_movies(movie_id: str, size: int = 10):
    """
    Recommend movies based on a given movie ID.
    """
    try:
        recommendations = await movie_service.recommend(movie_id=movie_id, top_k=size)
        return JSONResponse(content=recommendations, status_code=200)
    except Exception as e:
        logging.error(f"Error recommending movies: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/showtimes")
async def get_showtimes():
    """
    Get showtimes for movies.
    """
    try:
        showtimes = await movie_service.get_cinestar_showtimes()
        return JSONResponse(content=showtimes, status_code=200)
    except Exception as e:
        logging.error(f"Error fetching showtimes: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/showtimes/{id}")
async def get_showtimes(id: str):
    """
    Get showtimes for movies.
    """
    try:
        showtimes = await movie_service.get_cinestar_showtimes()
        return JSONResponse(content=showtimes[int(id)], status_code=200)
    except Exception as e:
        logging.error(f"Error fetching showtimes: {e}")
        raise HTTPException(status_code=500, detail=str(e))    