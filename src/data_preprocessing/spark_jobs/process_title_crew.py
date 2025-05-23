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

title_crew_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("directors", StringType(), True),  # comma-separated nconsts
    StructField("writers", StringType(), True)     # comma-separated nconsts
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

crew_df = read_data(spark, "/home/data/title_crew.csv", schema=title_crew_schema)
movie_df = read_data(spark, "/home/data/movies_2020_new.csv", schema=movie_schema)

crew_df = movie_df.alias("df1").\
    join(crew_df.alias("df2"), "tconst", "left").\
    select(
        col("df1.tconst"),
        col("df2.directors"),
        col("df2.writers")
    )

crew_df = crew_df.withColumn("directors", F.split(col("directors"), ","))
crew_df = crew_df.withColumn("directors", F.coalesce(col("directors"), F.array(F.lit("None"))))
crew_df = crew_df.withColumn("directors", F.explode(col("directors")))

crew_df = crew_df.withColumn("writers", F.split(col("writers"), ","))
crew_df = crew_df.withColumn("writers", F.coalesce(col("writers"), F.array(F.lit("None")))) 
crew_df = crew_df.withColumn("writers", F.explode(col("writers")))

# crew_df.where(col("tconst")=="tt0000001").show(10)
save_data(crew_df, "/home/data/new_title_crew")