from db.mongo_client import MongoClient
from db.es import ElasticSearchClient

from core.movie import get_current_year

from typing import List, Dict, Any


class MovieService:
    def __init__(self, mongo_client: MongoClient, es_client: ElasticSearchClient):
        """
        Initialize the MovieService with a MongoDB client.

        Args:
            mongo_client (MongoClient): The MongoDB client instance.
        """
        self.mongo_client = mongo_client
        self.es_client = es_client
        self.mongo_client.connect()
        self.es_client.connect()

    async def get_movies(self, collection_name: str = "movies", page: int = 0, offset: int = 20) -> List[Dict[str, Any]]:
        """
        Retrieve all movies from the database.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        collection = self.mongo_client.get_collection(collection_name)
        # Calculate the skip value based on the page number and offset
        skip = page * offset
        current_year = get_current_year()
        # movies = await collection\
        # .find({ "startYear": current_year},{"_id": 0, "tconst": 1, "primaryTitle": 1, "startYear": 1, "genres": 1, "posterPath": 1, "description": 1})\
        # .sort([("startYear",-1),("tconst",-1)])\
        # .skip(skip).limit(offset).to_list()  # Adjust the length as needed
        # return movies
        pipeline = [
            { "$match": { "startYear": current_year } },
            { "$lookup": {
                "from": "ratings",
                "localField": "tconst",
                "foreignField": "tconst",
                "as": "rating"
            }},
            { "$unwind": "$rating" },
            { "$sort": { "rating.numVotes": -1,"rating.averageRating": -1 } },
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
                "rating": "$rating.averageRating",
                "numVotes": "$rating.numVotes",
                "description": 1
            }}
        ]
        return await collection.aggregate(pipeline).to_list()
    
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
                "description": 1
            }}
        ]
        movie_collection = self.mongo_client.get_collection("movies")
        return await movie_collection.aggregate(pipeline).to_list(length=30)
    
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
        # Calculate the skip value based on the page number and page size
        skip = page * offset
        sorted_ratings_collection = self.mongo_client.get_collection("ratings")
        pipeline = [
            { "$sort": { "averageRating": -1 , "numVotes": -1} },
            { "$skip": skip },
            { "$limit": offset },
            {
                "$lookup": {
                    "from": "movies",
                    "localField": "tconst",
                    "foreignField": "tconst",
                    "as": "movies"
                }
            },
            { "$unwind": "$movies" },
            { "$project": {
                "_id": 0,
                "tconst": "$tconst",
                "averageRating": 1,
                "numVotes": 1,
                "primaryTitle": "$movies.primaryTitle",
                "startYear": "$movies.startYear",
                "genres": "$movies.genres",
                "posterPath": "$movies.posterPath",
                "description": "$movies.description"}
            }
        ]
        return await sorted_ratings_collection.aggregate(pipeline).to_list()
    
    

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
    
    async def search_movie_by_name(self, name: str = "") -> List[Dict[str, Any]]:
        """
        Retrieve movies by name.

        Args:
            name (str): The name of the movie.
            es_client (ElasticSearchClient): The ElasticSearch client instance.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        results = await self.es_client.fuzzy_search(index="movie", field="primaryTitle", value=name)
        return [hit["_source"] for hit in results["hits"]["hits"]]
    
    async def search_movie_by_director(self, name: str = "") -> List[Dict[str, Any]]:
        """
        Retrieve movies by director.

        Args:
            director (str): The name of the director.

        Returns:
            List[Dict[str, Any]]: A list of movies.
        """
        results = await self.es_client.fuzzy_search(index="movie", field="directors", value=name)
        return [hit["_source"] for hit in results["hits"]["hits"]]
    
    
    
async def main():
    # Example usage
    mongo_client = MongoClient("mongodb://root:example@localhost:27017", "movie_db")
    es_client = ElasticSearchClient("http://localhost:9200", "elastic", "changeme")
    mongo_client.connect()
    es_client.connect()
    movie_service = MovieService(mongo_client, es_client)
    
    print("=== Get Movies ===")
    movies = await movie_service.get_movie_description_by_tconst("tt0070596")
    # print(movies)
    # print(type(movie[0]["genres"]))
    for movie in movies:
        print(movie)
        print("===")
    
    # Close the database connection
    mongo_client.close()
    await es_client.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())