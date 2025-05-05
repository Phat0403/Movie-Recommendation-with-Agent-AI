from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd
import csv
import sys
csv.field_size_limit(sys.maxsize)
INDEX = "movie"

# Initialize the Elasticsearch client
es = Elasticsearch(
    ['http://localhost:9200'],
    basic_auth=('elastic', 'changeme'),
)
def bulk_data_to_elasticsearch(file_path: str = "/data/movie_director.csv", index: str = "movie") -> None:
    """
    Bulk insert data into Elasticsearch.
    """
    # Read the CSV file
    df = pd.read_csv(file_path, encoding='utf-8', sep="\t", engine="python", on_bad_lines='warn')
    df = df.fillna("None")
    # Convert DataFrame to dictionary
    docs = df.to_dict(orient='records')
    
    # Prepare the documents for bulk insertion
    docs = [
        {
            "_index": index,
            "_id": str(doc["tconst"]),
            "_source": doc
        }
        for doc in docs
    ]
    
    # Perform bulk insertion
    response = bulk(es, docs, raise_on_error=True)
    return response

def delete_index(index_name: str = "movie") -> None:
    """
    Delete an index in Elasticsearch.
    """
    response = es.indices.delete(index=index_name)
    return response

def insert_to_elastic_search(file_path: str = "/data/movie_director.csv", index: str = "movie") -> None:
    """
    Bulk insert data into Elasticsearch.
    """
    # Read the CSV file
    df = pd.read_csv(file_path, encoding='utf-8', sep="\t", engine="python", on_bad_lines='warn')
    df = df.fillna("None")
    # Convert DataFrame to dictionary
    docs = df.to_dict(orient='records')
    
    # Prepare the documents for bulk insertion
    docs = [
        {
            "_index": index,
            "_id": str(doc["tconst"]),
            "_source": doc
        }
        for doc in docs
    ]

    for doc in docs:
        # Insert each document into Elasticsearch
        try:
            es.index(index=index, id=doc["_id"], body=doc["_source"])
        except Exception as e:
            print(f"Error inserting document with ID: {doc['_id']}. Error: {e}")

# response = fuzzy_search_by_movie_name("The Spider-Man 2")
# for hit in response['hits']['hits']:
#     print(hit["_source"])
#     print("===")
if __name__ == "__main__":
    mappings = {
        "properties": {
            "tconst": { "type": "keyword" },

            "primaryTitle": {
                "type": "text",
                "fields": { "raw": { "type": "keyword" } }
            },

            "startYear":    { "type": "integer" },

            # genres là TEXT (full‑text search) + sub‑field raw (keyword)
            "genres": {
                "type": "text",
                "fields": { "raw": { "type": "keyword" } }
            },

            "posterPath":   { "type": "keyword", "index": False },

            "description":  { "type": "text", "analyzer": "english" },

            "directors": {
                "type": "text",
                "fields": { "raw": { "type": "keyword" } }
            }
        }
    }
    if es.indices.exists(index=INDEX):
        es.indices.delete(index=INDEX)
        print(f"Đã xoá index cũ: {INDEX}")
    response = bulk_data_to_elasticsearch("data/movie_director.csv")
    print(response)