from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, length
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
    StructField("numVotes", FloatType(), True)
])

movie_df = read_data(spark, "/home/data/movies_2020_new.csv", schema=movie_schema)
ratings_df = read_data(spark, "/home/data/title_ratings.csv", schema=title_ratings_schema)

# Fill averageRating and numVotes with 0 if they are null
ratings_df = ratings_df.withColumn("averageRating", F.when(col("averageRating").isNull(), 0).otherwise(col("averageRating")))
ratings_df = ratings_df.withColumn("numVotes", F.when(col("numVotes").isNull(), 0).otherwise(col("numVotes")))

new_ratings_df = movie_df.alias("df1").\
                join(ratings_df.alias("df2"), "tconst", "left").\
                where(col("df1.tconst").isNotNull()).\
                select(
                    col("df1.tconst"),
                    col("averageRating"),
                    col("numVotes")
                )

save_data(new_ratings_df, "/home/data/new_title_ratings")
