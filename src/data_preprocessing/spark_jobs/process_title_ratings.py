from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, broadcast
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

def read_data(spark, file_path, schema=None):
    """
    Read the CSV file into a DataFrame.
    """
    df = spark.read.csv(file_path, schema=schema, header=True)
    return df

def save_data(df, file_path):
    """
    Save the DataFrame to a CSV file.
    """
    df.write.csv(file_path, header=True, mode='overwrite')

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Data Preprocessing") \
    .config("spark.driver.maxResultSize", "2g") \
    .getOrCreate()

movie_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("titleType", StringType(), True),
    StructField("primaryTitle", StringType(), True),
    StructField("originalTitle", StringType(), True),
    StructField("isAdult", IntegerType(), True),
    StructField("startYear", StringType(), True),         # might be "\N"
    StructField("runtimeMinutes", StringType(), True),    # might be "\N"
    StructField("genres", StringType(), True),            # comma-separated
    StructField("posterPath", StringType(), True),
    StructField("backdropPath", StringType(), True),
    StructField("trailerPath", StringType(), True),
    StructField("description", StringType(), True)
])

title_ratings_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("averageRating", FloatType(), True),
    StructField("numVotes", IntegerType(), True)
])

movie_df = read_data(spark, "/home/data/movies_2020_new.csv", schema=movie_schema)
ratings_df = read_data(spark, "/home/data/title_ratings.csv", schema=title_ratings_schema)

new_ratings_df = movie_df.alias("df1").\
                join(ratings_df.alias("df2"), "tconst", "left").\
                select(
                    col("df1.tconst"),
                    col("averageRating"),
                    col("numVotes")
                )

save_data(new_ratings_df, "/home/data/new_title_ratings")
