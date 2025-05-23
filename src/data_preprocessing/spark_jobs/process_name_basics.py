from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col, broadcast, explode, split
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

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
    .appName("Process name basics") \
    .getOrCreate()

name_basics_schema = StructType([
    StructField("nconst", StringType(), True),
    StructField("primaryName", StringType(), True),
    StructField("birthYear", IntegerType(), True),
    StructField("deathYear", IntegerType(), True),
    StructField("primaryProfession", StringType(), True),
    StructField("knownForTitles", StringType(), True)
])

principal_schema = StructType([
    StructField("tconst", StringType(), True),
    StructField("ordering", IntegerType(), True),
    StructField("nconst", StringType(), True),
    StructField("category", StringType(), True),
    StructField("job", StringType(), True),
    StructField("characters", StringType(), True)
])

name_basics_df = read_data(spark, "/home/data/name_basics.csv", schema=name_basics_schema)

# name_basics_df = name_basics_df.withColumn("knownForTitles", split(col("knownForTitles"), ","))
# name_basics_df.withColumn("knownForTitles", F.coalesce(col("knownForTitles"), F.array(F.lit("None"))))
# name_basics_df = name_basics_df.\
#                 withColumn("tconst", explode(col("knownForTitles"))).\
#                 drop("knownForTitles")
                
principal_df = read_data(spark, "/home/data/new_title_principals", schema=principal_schema)
principal_df = principal_df.repartition(16)
new_name_basics_df = principal_df.alias("df1").\
                join(name_basics_df, "nconst", "left").\
                select(
                    col("nconst"),
                    col("primaryName"),
                    col("birthYear"),
                    col("deathYear"),
                    col("primaryProfession"),
                    col("knownForTitles")
                ).\
                dropDuplicates(["nconst"]).\
                dropna(subset=["nconst"])

# Save the DataFrame to a CSV file
save_data(new_name_basics_df, "/home/data/new_name_basics")

