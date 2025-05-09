from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, broadcast
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, ArrayType

def read_data(spark, file_path, schema=None):
    """
    Read the CSV file into a DataFrame.
    """
    df = spark.read.csv(file_path, schema=schema, header=True, sep = ",")
    return df

def save_data(df, file_path):
    """
    Save the DataFrame to a CSV file.
    """
    df.write.csv(file_path, header=True, mode='overwrite', sep=",")

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("Data Preprocessing") \
    .config("spark.driver.maxResultSize", "2g") \
    .getOrCreate()

principal_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("ordering", IntegerType(), True),
    StructField("nconst", StringType(), True),
    StructField("category", StringType(), True),
    StructField("job", StringType(), True),
    StructField("characters", StringType(), True)
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

principal_df = read_data(spark, "/home/data/title_principals.csv", schema=principal_schema)
principal_df = principal_df.withColumn("characters", F.split(col("characters"), ","))
principal_df = principal_df.withColumn("characters", F.coalesce(col("characters"), F.array(F.lit("None"))))
principal_df = principal_df.withColumn("characters", F.explode(col("characters")))
principal_df = principal_df.withColumn("characters", F.trim(col("characters")))
principal_df = principal_df.withColumn("characters", F.regexp_replace(col("characters"), "\"", ""))
principal_df = principal_df.withColumn("characters", F.regexp_replace(col("characters"), "[\\[\\]]", ""))
movie_df = read_data(spark, "/home/data/movies_2020_new.csv", schema=movie_schema)
principal_df = principal_df.repartition(16)
new_principal_df = movie_df.alias("df1").\
                join(principal_df.alias("df2"), "tconst", "left").\
                select(
                    col("df1.tconst"),
                    col("df2.ordering"),
                    col("df2.nconst"),
                    col("df2.category"),
                    col("df2.job"),
                    col("df2.characters")
                )

# new_principal_df.show(100)
save_data(new_principal_df, "/home/data/new_title_principals")