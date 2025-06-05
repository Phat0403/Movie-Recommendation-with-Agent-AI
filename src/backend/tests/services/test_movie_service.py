import pytest
from unittest.mock import AsyncMock, MagicMock
from services.movie import MovieService
from core.utils import get_current_year, get_current_date

@pytest.fixture
def movie_service():
    mongo = MagicMock()
    es = AsyncMock()
    redis = AsyncMock()
    chroma = MagicMock()
    service = MovieService(mongo, es, redis, chroma)
    return service

@pytest.mark.asyncio
async def test_get_movies(movie_service):
    mock_collection = MagicMock()
    mock_aggregate = AsyncMock()
    mock_aggregate.to_list.return_value = [{"primaryTitle": "Test Movie"}]
    mock_collection.aggregate.return_value = mock_aggregate
    movie_service.mongo_client.get_collection.return_value = mock_collection

    result = await movie_service.get_movies()
    assert result == [{"primaryTitle": "Test Movie"}]

@pytest.mark.asyncio
async def test_get_all_movies(movie_service):
    mock_collection = MagicMock()
    mock_aggregate = AsyncMock()
    mock_aggregate.to_list.return_value = [{"primaryTitle": "All Movie"}]
    mock_collection.aggregate.return_value = mock_aggregate
    movie_service.mongo_client.get_collection.return_value = mock_collection

    result = await movie_service.get_all_movies(year=2023)
    assert result[0]["primaryTitle"] == "All Movie"

@pytest.mark.asyncio
async def test_get_movies_by_list_tconst(movie_service):
    mock_collection = MagicMock()
    mock_find = AsyncMock()
    mock_find.to_list.return_value = [{"tconst": "tt001"}]
    mock_collection.find.return_value = mock_find
    movie_service.mongo_client.get_collection.return_value = mock_collection

    result = await movie_service.get_movies_by_list_tconst(["tt001"])
    assert result[0]["tconst"] == "tt001"

@pytest.mark.asyncio
async def test_get_movie_description_by_tconst(movie_service):
    mock_collection = MagicMock()
    mock_aggregate = AsyncMock()
    mock_aggregate.to_list.return_value = [{"tconst": "tt002"}]
    mock_collection.aggregate.return_value = mock_aggregate
    movie_service.mongo_client.get_collection.return_value = mock_collection

    result = await movie_service.get_movie_description_by_tconst("tt002")
    assert result[0]["tconst"] == "tt002"

@pytest.mark.asyncio
async def test_get_movies_by_genre(movie_service):
    mock_collection = MagicMock()

    # Tạo chuỗi mock cho find().sort().skip().limit().to_list()
    mock_find = MagicMock()
    mock_sort = MagicMock()
    mock_skip = MagicMock()
    mock_limit = MagicMock()
    mock_limit.to_list = AsyncMock(return_value=[{"genres": "Drama"}])

    mock_skip.limit.return_value = mock_limit
    mock_sort.skip.return_value = mock_skip
    mock_find.sort.return_value = mock_sort

    mock_collection.find.return_value = mock_find
    movie_service.mongo_client.get_collection.return_value = mock_collection

    result = await movie_service.get_movies_by_genre("Drama")
    assert result[0]["genres"] == "Drama"

@pytest.mark.asyncio
async def test_get_movies_by_ratings(movie_service):
    mock_collection = MagicMock()
    mock_aggregate = AsyncMock()
    mock_aggregate.to_list.return_value = [{"rating": 8.5}]
    mock_collection.aggregate.return_value = mock_aggregate
    movie_service.mongo_client.get_collection.return_value = mock_collection

    result = await movie_service.get_movies_by_ratings()
    assert result[0]["rating"] == 8.5

@pytest.mark.asyncio
async def test_get_movies_by_trending(movie_service):
    mock_collection = MagicMock()
    mock_aggregate = AsyncMock()
    mock_aggregate.to_list.return_value = [{"tconst": "tt003"}]
    mock_collection.aggregate.return_value = mock_aggregate
    movie_service.mongo_client.get_collection.return_value = mock_collection

    result = await movie_service.get_movies_by_trending()
    assert result[0]["tconst"] == "tt003"

@pytest.mark.asyncio
async def test_get_movies_by_numVote(movie_service):
    mock_collection = MagicMock()
    mock_aggregate = AsyncMock()
    mock_aggregate.to_list.return_value = [{"numVotes": 1000}]
    mock_collection.aggregate.return_value = mock_aggregate
    movie_service.mongo_client.get_collection.return_value = mock_collection

    result = await movie_service.get_movies_by_numVote()
    assert result[0]["numVotes"] == 1000

@pytest.mark.asyncio
async def test_get_movies_by_nconst(movie_service):
    mock_collection = MagicMock()
    mock_aggregate = AsyncMock()
    mock_aggregate.to_list.return_value = [{"tconst": "tt004"}]
    mock_collection.aggregate.return_value = mock_aggregate
    movie_service.mongo_client.get_collection.return_value = mock_collection

    result = await movie_service.get_movies_by_nconst("nm001")
    assert result[0]["tconst"] == "tt004"

@pytest.mark.asyncio
async def test_search_movie_by_name(movie_service):
    movie_service.es_client.fuzzy_search.return_value = {
        "hits": {"hits": [{"_source": {"primaryTitle": "Search Movie"}}]}
    }
    result = await movie_service.search_movie_by_name("Search")
    assert result[0]["primaryTitle"] == "Search Movie"

@pytest.mark.asyncio
async def test_search_movie_by_director(movie_service):
    movie_service.es_client.fuzzy_search.return_value = {
        "hits": {"hits": [{"_source": {"directors": "John Doe"}}]}
    }
    result = await movie_service.search_movie_by_director("John")
    assert result[0]["directors"] == "John Doe"

@pytest.mark.asyncio
async def test_get_cinestar_showtimes_cache_hit(movie_service):
    today = get_current_date()
    movie_service.redis_client.get.return_value = '[{"title": "Cached Show"}]'
    result = await movie_service.get_cinestar_showtimes()
    assert result[0]["title"] == "Cached Show"

@pytest.mark.asyncio
async def test_get_cinestar_showtimes_cache_miss(movie_service):
    today = get_current_date()
    movie_service.redis_client.get.return_value = None
    movie_service.fetch_cinestar_showtimes = AsyncMock(return_value=[{"title": "Live Show"}])
    movie_service.redis_client.set = AsyncMock()

    result = await movie_service.get_cinestar_showtimes()
    assert result[0]["title"] == "Live Show"

@pytest.mark.asyncio
async def test_recommend(movie_service):
    movie_service.get_movie_description_by_tconst = AsyncMock(return_value=[{"description": "some desc"}])
    movie_service.redis_client.get.return_value = None
    movie_service.chroma_client.query.return_value = {"ids": [["tt001", "tt002"]]}
    movie_service.get_movies_by_list_tconst = AsyncMock(return_value=[{"tconst": "tt001"}, {"tconst": "tt002"}])
    movie_service.redis_client.set = AsyncMock()

    result = await movie_service.recommend("tt001")
    assert len(result) == 2


