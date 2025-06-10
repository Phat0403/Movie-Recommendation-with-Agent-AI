import chromadb

from utils.common_functions import read_yaml
from config.db_config import CHROMA_DB_PATH
from core.embedder import CustomEmbeddingFunction

class ChromaDBClient:
    def __init__(self, config_path: str = "config/movie_embedding_config.yaml"):
        self.embedder_config = read_yaml(config_path)
        self.client = chromadb.PersistentClient(
            path='./chroma'
        )
        self.model = self.embedder_config.get("model_name", "intfloat/multilingual-e5-base")
        self.embedding_function = CustomEmbeddingFunction(self.model)
        self.collection_name = self.embedder_config.get("collection_name", "movie")
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function
        )
    
    def query(self, query_text: str, n_results: int = 10):
        """
        Query the ChromaDB collection with a text input.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
    
    def query_by_embedding(self, embedding_vector, n_results: int = 10):
        """
        Query the ChromaDB collection with an embedding vector.
        """
        results = self.collection.query(
            query_embeddings=[embedding_vector],
            n_results=n_results
        )
        return results
    
    def embed_movie(self, movies_description):
        """
        Embed movie descriptions into the vector.
        """
        return self.embedding_function(movies_description)
        
    
if __name__ == "__main__":
    
    chroma_client = ChromaDBClient()
    # print("Collections available:", chroma_client.client.list_collections())
    # print(type(chroma_client.client))
    # print(type(chroma_client.collection))
    query_text = "horror movie"
    results = chroma_client.query(query_text)
    # print(f"Query results for '{query_text}':")
    # print(results["documents"])
    # print("Metadata:", results["metadatas"])
    # print("IDs:", results["ids"])
    # print("URIs:", results["uris"])
    ids = results.get("ids", [])[0]
    documents = results.get("documents", [])[0]
    results = [ids[i]+ ": " + documents[i] for i in range(len(ids))]
    print(results)