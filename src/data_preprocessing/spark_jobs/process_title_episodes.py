from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, broadcast
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, ArrayType

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

title_episode_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("parentTconst", StringType(), True),
    StructField("seasonNumber", StringType(), True),
    StructField("episodeNumber", StringType(), True)
])

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

movie_df = read_data(spark, "/home/data/movies_2020_new.csv", schema=movie_schema)
episode_df = read_data(spark, "/home/data/title_episodes.csv", schema=title_episode_schema)

episode_df = movie_df.alias("df1").\
        join(episode_df.alias("df2"), "tconst", "left").\
        select(
            col("df1.tconst"),
            col("df2.parentTconst"),
            col("df2.seasonNumber"),
            col("df2.episodeNumber")
        )

episode_df.where(col("parentTconst").isNotNull()).show(50)