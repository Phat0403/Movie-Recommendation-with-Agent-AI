import torch.nn.functional as F

from torch import Tensor
from transformers import AutoTokenizer, AutoModel

def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

class Embedder:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed(self, texts: list[str]) -> Tensor:
        batch_dict = self.tokenizer(texts, max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = self.model(**batch_dict)
        embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
        return F.normalize(embeddings, p=2, dim=1)
    
if __name__ == "__main__":
    # Example usage
    embedder = Embedder("intfloat/multilingual-e5-base")
    input_texts = ["query: tt32001464_Utopia_Utopia_['Action', 'Thriller']_A soldier searching for his missing wife breaks into a high-tech facility, believing she's been caught in a human trafficking ring. But beyond its walls, he finds a surreal, futuristic fantasy park where reality and illusion blur. As he navigates this seductive and dangerous world, a shocking truth pulls him deeper into a deadly game where nothing is as it seems._['Moe Dunford', 'Charlotte Vega', 'Michael D. Xavier', 'Alix Villaret', 'Wanda Banda', 'Maddy Ambus', 'Jade Coatsworth', 'Daniel Bernhardt', 'Lucy Akhurst', 'Philipp Boos', 'Rich Walters', 'Frank Meyer', 'Trevor Mirosh', 'Fern Champion', 'Preslava Hristova', 'Ivan Ranghelov']",
                'query: Utopia']
    embeddings = embedder.embed(input_texts)
    scores = (embeddings[:1] @ embeddings[1:].T) * 100
    print(scores)