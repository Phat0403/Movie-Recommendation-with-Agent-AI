from pydantic import BaseModel, Field

class Movie(BaseModel):
    tconst: str = Field(..., description="The unique identifier for the movie")
    primaryTitle: str = Field(..., description="The primary title of the movie")
    startYear: int = Field(..., description="The year the movie was released")
    genres: str = Field(..., description="The genres of the movie")
    posterPath: str = Field(..., description="The path to the movie poster")
    description: str = Field(..., description="A brief description of the movie")

class MovieWithRating(Movie):
    rating: float = Field(..., description="The rating of the movie")
    numVotes: int = Field(..., description="The number of votes for the movie")

class MovieDetails(Movie):
    isAdult: bool = Field(..., description="Is the movie for adults")
    rating: float = Field(..., description="The rating of the movie")
    numVotes: int = Field(..., description="The number of votes for the movie")
    nconst: list[str] = Field(..., description="List of unique identifier for actors")
    name: list[str] = Field(..., description="List of name of actors")
    backdropPath: str = Field(..., description="The path to the movie backdrop")
    trailerPath: str = Field(..., description="The path to the movie trailer")

class MovieInES(Movie):
    directors: str = Field(..., description="The directors of the movie")

class MovieList(BaseModel):
    movies: list[Movie] = Field(..., description="List of movies")

class MovieWithRatingList(BaseModel):
    movies: list[MovieWithRating] = Field(..., description="List of movies with ratings")

class MovieInESList(BaseModel):
    movies: list[MovieInES] = Field(..., description="List of movies in Elasticsearch")