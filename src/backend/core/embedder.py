import os
import torch
import torch.nn.functional as F
from torch import Tensor
from tqdm import tqdm
import chromadb
from chromadb.utils.embedding_functions import EmbeddingFunction
from transformers import AutoTokenizer, AutoModel

# Trung bình embedding có attention mask
def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    mask = attention_mask.unsqueeze(-1).expand(last_hidden_states.size()).float()
    masked_embeddings = last_hidden_states * mask
    summed = masked_embeddings.sum(dim=1)
    counts = mask.sum(dim=1)
    return summed / counts

# Embedder sử dụng GPU
class Embedder:
    def __init__(self, model_name: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)

    def embed(self, texts: list[str]) -> Tensor:
        batch_dict = self.tokenizer(
            texts,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors='pt'
        )
        batch_dict = {k: v.to(self.device) for k, v in batch_dict.items()}

        with torch.no_grad():
            outputs = self.model(**batch_dict)
            embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
            return F.normalize(embeddings, p=2, dim=1)

# Wrapper cho Chroma
class CustomEmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name: str):
        self.embedder = Embedder(model_name)

    def __call__(self, texts: list[str]) -> list[list[float]]:
        return self.embedder.embed(texts).tolist()

# Main pipeline
class MovieEmbedder:
    def __init__(self):
        self.data_path = "/kaggle/input/movie-description/movie_description.txt"
        self.model_name = "intfloat/multilingual-e5-base"
        self.chroma_db_path = "./chroma"
        self.collection_name = "movie"

    def load_data(self):
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return f.readlines()

    def get_chroma_collection_client(self):
        chroma_client = chromadb.PersistentClient(path=self.chroma_db_path)
        return chroma_client, chroma_client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=CustomEmbeddingFunction(self.model_name)
        )

    def embed_movie(self, movies_descriptions, collection):
        for i in tqdm(range(0, len(movies_descriptions), 32)):
            batch = [movie.strip() for movie in movies_descriptions[i:i+32]]
            try:
                ids = [line.split('_', 1)[0] for line in batch]
                names = [line.split('_', 1)[1] for line in batch]
                collection.upsert(
                    documents=batch,
                    metadatas=[{"name": name} for name in names],
                    ids=ids
                )
            except Exception as e:
                print(batch)
                print(f"Error on batch {i//32}: {e}")
                return
            
if __name__ == "__main__":
    embedder = Embedder("intfloat/multilingual-e5-base")
    query = "Test movie description"
    embedding = embedder.embed([query])
    movie_embedder = MovieEmbedder()
    client, collection = movie_embedder.get_chroma_collection_client()
    # print(client.get_status())
    print(client.list_collections())
    print(client.get_user_identity())
    print(f"Collection name: {collection.name}")
    print(f"Collection metadata: {collection.metadata}")
    print(f"Collection embedding function: {collection.get()}")
    print(f"Collection embedding function: {collection._embedding_function}")
    documents = collection.get()['documents']
    print(f"Number of documents in collection: {len(documents)}")    