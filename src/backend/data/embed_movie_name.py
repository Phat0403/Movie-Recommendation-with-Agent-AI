from utils.common_functions import read_yaml
from ai.embedder import Embedder
from utils.logger import get_logger
import chromadb

logger = get_logger(__name__)

class EmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self, embedder: Embedder):
        self.embedder = embedder

    def __call__(self, texts: list[str]) -> list[list[float]]:
        """
        Embed a list of texts using the specified embedder.

        Args:
            texts (list[str]): List of texts to embed.

        Returns:
            list[list[float]]: List of embeddings for each text.
        """
        return self.embedder.embed(texts).tolist()

class MovieEmbedder:
    def __init__(self):
        logger.info("Initializing MovieEmbedder")
        self.movie_embedding_config = read_yaml("config/movie_embedding_configs.yaml")
        self.data_path = self.movie_embedding_config['data_path']
        self.model = self.movie_embedding_config['model']
        self.embedder = Embedder(self.model)
        self.chroma_db_path = self.movie_embedding_config['chroma_db_path']
        self.collection_name = self.movie_embedding_config['collection_name']

    def load_data(self):
        """
        Load the movie data from the specified path.
        """
        # Placeholder for loading data
        logger.info("Loading movie data")
        movies_descriptions = open(self.data_path, 'r').readlines()
        return movies_descriptions
    
    def get_chroma_collection_client(self):
        """
        Create a Chroma client for embedding.
        """
        chroma_client = chromadb.PersistentClient(
            path=self.chroma_db_path
        )
        collection = chroma_client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=EmbeddingFunction(self.embedder)
        )
        return collection

    def embed_movie(self, movies_descriptions, chroma_client_collection):
        """
        Embed the movie names using the loaded model.
        """
        logger.info("Embedding movie description started")
        for i in range(0, len(movies_descriptions), 32):
            logger.info(f"Processing batch {i//32 + 1}/{len(movies_descriptions)//32}")
            movies_batch = movies_descriptions[i:min(i+32,len(movies_descriptions))]
            movies_ids = [movie.split('_')[0] for movie in movies_batch]
            movies_names = [movie.split('_')[1] for movie in movies_batch]
            chroma_client_collection.upsert(
                documents=movies_batch,
                metadatas=[{"name": name} for name in movies_names],
                ids=movies_ids
            )
        logger.info("Embedding movie description finished")

    def run(self):
        """
        Run the entire embedding process.
        """
        movie_desc = self.load_data()
        collection = self.get_chroma_collection_client()
        self.embed_movie(movie_desc, collection)

if __name__ == "__main__":
    movie_embedder = MovieEmbedder()
    movie_embedder.run()

    collection = movie_embedder.get_chroma_collection_client()
    result = collection.query(
        query_texts=["Utopia"],
        n_results=10
    )
    
    for res in result["documents"][0]:
        print(f"{res} \n")