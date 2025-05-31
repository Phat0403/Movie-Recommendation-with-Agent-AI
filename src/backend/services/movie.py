from db.mongo_client import MongoClient
from db.es import ElasticSearchClient
from db.redis_client import RedisClient
from db.chroma import ChromaDBClient

from core.utils import get_current_year, get_current_date
from typing import List, Dict, Any

from core.selenium_util import go_to_url, get_driver, get_link_from_elements, get_movie_info_from_link
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

import json

class MovieService:
    def __init__(self, mongo_client: MongoClient, es_client: ElasticSearchClient, redis_client: RedisClient, chroma_client: ChromaDBClient):
        """
        Initialize the MovieService with a MongoDB client.

        Args:
            mongo_client (MongoClient): The MongoDB client instance.
        """
        self.mongo_client = mongo_client
        self.es_client = es_client
        self.redis_client = redis_client
        self.chroma_client = chroma_client
        self.mongo_client.connect()
        self.es_client.connect()

    async def get_movies(self, collection_name: str = "movies", page: int = 0, offset: int = 20) -> List[Dict[str, Any]]:
        """
        Retrieve all movies from the database.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        collection = self.mongo_client.get_collection(collection_name)
        skip = page * offset
        current_year = get_current_year()
        
        pipeline = [
            { "$match": { "startYear": current_year } },
            { "$sort": { "release_date": -1 } },
            { "$skip": skip },
            { "$limit": offset },
            { "$project": {
                "_id": 0,
                "tconst": 1,
                "primaryTitle": 1,
                "startYear": 1,
                "genres": 1,
                "posterPath": 1,
                "backdropPath": 1,
                "release_date": 1,
                "rating": "$averageRating",
                "numVotes": 1,
                "description": 1
            }}
        ]
        movies = await collection.aggregate(pipeline).to_list(length=None)
        return movies
    async def get_all_movies(self, collection_name: str = "movies",year: int =0, genre: str = "",sort: int =0, page: int = 0, offset: int = 20) -> List[Dict[str, Any]]:
        """
        Retrieve all movies from the database.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        collection = self.mongo_client.get_collection(collection_name)
        # Get total count of documents in the collection
        skip = page * offset
        # Build the filter dynamically
        filter_query = {}
        if year != 0:
            filter_query["startYear"] = int(year)
        if genre:
            filter_query["genres"] =  { "$regex": genre, "$options": "i" }
        pipeline = [
        { "$match": filter_query }
    ]
        if sort != 0:
            print("have_sort", sort)
            pipeline.append({ "$sort": { "averageRating": sort } }) 
        pipeline.extend([
            { "$match": filter_query },
            { "$skip": skip },
            { "$limit": offset },
            { "$project": {
                "_id": 0,
                "tconst": 1,
                "primaryTitle": 1,
                "startYear": 1,
                "genres": 1,
                "posterPath": 1,
                "backdropPath": 1,
                "release_date": 1,
                "rating": "$averageRating",
                "numVotes": 1,
                "description": 1
            }}
        ])
        movies = await collection.aggregate(pipeline).to_list(length=None)
        return  movies
    
    async def get_movies_by_list_tconst(self, tconst_list: List[str], collection_name: str = "movies") -> List[Dict[str, Any]]:
        """
        Retrieve movies by a list of IDs.

        Args:
            tconst_list (List[str]): A list of movie IDs.
            collection_name (str): The name of the collection.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        collection = self.mongo_client.get_collection(collection_name)
        movies = await collection.find(
            { "tconst": { "$in": tconst_list } },
            {
                "_id": 0,
                "tconst": 1,
                "primaryTitle": 1,
                "startYear": 1,
                "genres": 1,
                "posterPath": 1,
                "backdropPath": 1,
                "release_date": 1,
                "rating": "$averageRating",
                "numVotes": 1,
                "description": 1
            }
        ).to_list(length=None)
        return movies
    
    async def get_movie_description_by_tconst(self, tconst: str = "") -> Dict[str, Any]:
        """
        Retrieve a movie description by its ID.

        Args:
            collection_name (str): The name of the collection.
            tconst (str): The ID of the movie.

        Returns:
            Dict[str, Any]: The movie description.
        """
        pipeline = [
            { "$match": { "tconst": tconst } },
            {
                "$lookup": {
                    "from": "principals",
                    "localField": "tconst",
                    "foreignField": "tconst",
                    "as": "principals"
                }
            },
            { "$unwind": "$principals" },
            { "$group": {
            "_id": "$_id",  
            "tconst": { "$first": "$tconst" },
            "primaryTitle": { "$first": "$primaryTitle" },
            "startYear": { "$first": "$startYear" },
            "genres": { "$first": "$genres" },
            "nconst": { "$addToSet": "$principals.nconst" },
            "posterPath": { "$first": "$posterPath" },
            "backdropPath": { "$first": "$backdropPath" },
            "release_date": { "$first": "$release_date" },
            "runtimeMinutes": { "$first": "$runtimeMinutes" },
            "trailerPath": { "$first": "$trailerPath" },
            "description": { "$first": "$description" }
            }
            },
            {
                "$lookup": {
                    "from": "ratings",
                    "localField": "tconst",
                    "foreignField": "tconst",
                    "as": "rating"
                }
            },
            {
                "$lookup": {
                    "from": "name_basics",
                    "localField": "nconst",
                    "foreignField": "nconst",
                    "as": "name_basics"
                }
            },
            { "$project": {
                "_id": 0,
                "tconst": 1,
                "primaryTitle": 1,
                "isAdult": 1,
                "startYear": 1,
                "runtimeMinutes": 1,
                "genres": 1,
                "rating": { "$arrayElemAt": ["$rating.averageRating", 0] },
                "numVotes": { "$arrayElemAt": ["$rating.numVotes", 0] },
                "name": "$name_basics.primaryName",
                "nconst": "$name_basics.nconst",
                "posterPath": 1,
                "backdropPath": 1,
                "trailerPath": 1,
                "release_date": 1,
                "description": 1
            }}
        ]
        movie_collection = self.mongo_client.get_collection("movies")
        return await movie_collection.aggregate(pipeline).to_list()
    
    async def get_movies_by_genre(self, genre: str = "", collection_name: str = "movies", page: int = 0, offset: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve movies by genre.

        Args:
            genre (str): The genre of the movie.
            collection_name (str): The name of the collection.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        collection = self.mongo_client.get_collection(collection_name)
        # Calculate the skip value based on the page number and page size
        skip = page * offset
        movies = await collection.find({
                "genres": { "$regex": genre, "$options": "i" }
            }, {"_id": 0, "tconst": 1, "primaryTitle": 1, "startYear": 1, "genres": 1, "posterPath": 1, "description": 1})\
            .sort([("startYear",-1),("tconst",-1)])\
            .skip(skip).limit(offset).to_list()  # Adjust the length as needed
        return movies
    
    async def get_movies_by_ratings(self, collection_name: str = "movies", page: int = 0, offset: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve movies by ratings.

        Args:
            rating (float): The rating of the movie.
            collection_name (str): The name of the collection.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        collection = self.mongo_client.get_collection(collection_name)
        skip = page * offset

        pipeline = [
            { "$sort": { "averageRating": -1 } },
            { "$skip": skip },
            { "$limit": offset },
            { "$project": {
                "_id": 0,
                "tconst": 1,
                "primaryTitle": 1,
                "startYear": 1,
                "genres": 1,
                "posterPath": 1,
                "backdropPath": 1,
                "release_date": 1,
                "rating": "$averageRating",
                "numVotes": 1,
                "description": 1
            }}
        ]
        movies = await collection.aggregate(pipeline).to_list(length=None)
        return movies
    async def get_movies_by_trending(self, collection_name: str = "movies", page: int = 0, offset: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve movies by ratings.

        Args:
            rating (float): The rating of the movie.
            collection_name (str): The name of the collection.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        collection = self.mongo_client.get_collection(collection_name)
        skip = page * offset
        current_year = get_current_year()
        pipeline = [
            { "$match": { "startYear": current_year } },
            { "$sort": { "weightTrending": -1 } },
            { "$skip": skip },
            { "$limit": offset },
            { "$project": {
                "_id": 0,
                "tconst": 1,
                "primaryTitle": 1,
                "startYear": 1,
                "genres": 1,
                "posterPath": 1,
                "backdropPath": 1,
                "release_date": 1,
                "rating": "$averageRating",
                "numVotes": 1,
                "description": 1
            }}
        ]
        movies = await collection.aggregate(pipeline).to_list(length=None)
        return movies
    
    async def get_movies_by_numVote(self, collection_name: str = "movies", page: int = 0, offset: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve movies by ratings.

        Args:
            rating (float): The rating of the movie.
            collection_name (str): The name of the collection.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        collection = self.mongo_client.get_collection(collection_name)
        skip = page * offset
        pipeline = [
            { "$sort": { "numVotes": -1 } },
            { "$skip": skip },
            { "$limit": offset },
            { "$project": {
                "_id": 0,
                "tconst": 1,
                "primaryTitle": 1,
                "startYear": 1,
                "genres": 1,
                "posterPath": 1,
                "backdropPath": 1,
                "release_date": 1,
                "rating": "$averageRating",
                "numVotes": 1,
                "description": 1
            }}
        ]
        movies = await collection.aggregate(pipeline).to_list(length=None)
        return movies

    async def get_movies_by_nconst(self, nconst: str = "") -> List[Dict[str, Any]]:
        """
        Retrieve movies by actor.

        Args:
            actor (str): The name of the actor.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        collection = self.mongo_client.get_collection("principals")

        pipeline = [
            { "$match": { "nconst": nconst } },
            {
                "$lookup": {
                    "from": "movies",
                    "localField": "tconst",
                    "foreignField": "tconst",
                    "as": "movies"
                }
            },
            { "$unwind": "$movies" },
            {
                "$group": {
                    "_id": "$movies.tconst",
                    "primaryTitle": { "$first": "$movies.primaryTitle" },
                    "startYear": { "$first": "$movies.startYear" },
                    "genres": { "$first": "$movies.genres" },
                    "posterPath": { "$first": "$movies.posterPath" },
                    "description": { "$first": "$movies.description" }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "tconst": "$_id",
                    "primaryTitle": 1,
                    "startYear": 1,
                    "genres": 1,
                    "posterPath": 1,
                    "description": 1
                }
            }
        ]

        return await collection.aggregate(pipeline).to_list()
    
    async def search_movie_by_name(self, name: str = "", size: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve movies by name.

        Args:
            name (str): The name of the movie.
            es_client (ElasticSearchClient): The ElasticSearch client instance.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        results = await self.es_client.fuzzy_search(index="movie", field="primaryTitle", value=name, size=size)
        return [hit["_source"] for hit in results["hits"]["hits"]]
    
    async def search_movie_by_director(self, name: str = "", size: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve movies by director.

        Args:
            director (str): The name of the director.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        results = await self.es_client.fuzzy_search(index="movie", field="directors", value=name, size=size)
        return [hit["_source"] for hit in results["hits"]["hits"]]
    
    async def fetch_cinestar_showtimes(self) -> List[Dict[str, Any]]:
        """
        Fetch showtimes from the Cinestar API.

        Returns:
            List[Dict[str, Any]]: A list of showtimes.
        """
        url = "https://www.cgv.vn/default/movies/now-showing.html"  # Replace with the actual URL
        driver = get_driver()
        
        try:
            go_to_url(driver, url)
            elements = driver.find_elements(By.XPATH, "//h2[@class='product-name']/a")
            links = get_link_from_elements(elements)
            # Use ThreadPoolExecutor to fetch data concurrently
            driver.quit()
            with ThreadPoolExecutor(max_workers=3) as executor:
                results = list(executor.map(get_movie_info_from_link, links))

        except Exception as e:
            print(f"Error fetching Cinestar showtimes: {e}")
            return []
        finally:
            return results

    async def get_cinestar_showtimes(self) -> List[Dict[str, Any]]:
        """
        Retrieve showtimes from Cinestar.

        Returns:
            List[Dict[str, Any]]: A list of showtimes.
        """
        today = get_current_date()    
        showtimes = await self.redis_client.get(f"cinestar_showtimes_{today}")    
        if showtimes is None:        
            # Fetch showtimes from the API and store them in Redis
            showtimes = await self.fetch_cinestar_showtimes()
            showtimes_string = json.dumps(showtimes)
            # Store the showtimes in Redis with an expiration time of 1 day
            expired_time = 24 * 60 * 60  # 1 day in seconds
            await self.redis_client.set(f"cinestar_showtimes_{today}", showtimes_string, expire=expired_time)
        else:
            # Deserialize the showtimes from Redis
            showtimes = json.loads(showtimes)
        return showtimes
    
    async def recommend(self, movie_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Recommend movies based on a given movie ID.

        Args:
            movie_id (str): The ID of the movie to base recommendations on.
            top_k (int): The number of recommendations to return.

        Returns:
            List[Dict[str, Any]]: A list of recommended movies.
        """
        movie = await self.get_movie_description_by_tconst(movie_id)
        movie = movie[0] if movie else None
        if not movie:
            raise ValueError(f"Movie with ID {movie_id} not found.")
        # Check if the movie is already cached in Redis
        cached_recommendations = await self.redis_client.get(f"movie_recommendations_{movie_id}")
        if cached_recommendations:
            recommended_movies = json.loads(cached_recommendations)
        else:
            results = self.chroma_client.query(movie["description"], n_results=top_k)
            movie_ids = results["ids"][0]
            recommended_movies = await self.get_movies_by_list_tconst(movie_ids)
            await self.redis_client.set(f"movie_recommendations_{movie_id}", json.dumps(recommended_movies), expire=60 * 60)  # Cache for 1 hour
        return recommended_movies
    
async def main():
    # Example usage
    mongo_client = MongoClient("mongodb://root:example@localhost:27017", "movie_db")
    es_client = ElasticSearchClient("http://localhost:9200", "elastic", "changeme")
    redis_client = RedisClient(host="localhost", port=6379, db=0, password=None)
    chroma_client = ChromaDBClient()
    movie_service = MovieService(mongo_client, es_client, redis_client, None)
    # result = await movie_service.recommend("tt10872600", 10)
    # print(result)
    
    # print("=== Get Movies ===")
    # movies = await movie_service.get_movie_description_by_tconst("tt0070596")
    # # print(movies)
    # # print(type(movie[0]["genres"]))
    # for movie in movies:
    #     print(movie)
    #     print("===")
    
    # # Close the database connection
    # mongo_client.close()
    # await es_client.close()
    await redis_client.delete(f"cinestar_showtimes_{get_current_date()}")
    result = await movie_service.get_cinestar_showtimes()
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())