from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings


class STVectorizer:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def vectorize(self, text: str) -> list:
        embedding = self.model.encode(text)
        return embedding.tolist()


class HFVectorizer:
    def __init__(self, model_name):
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}
        self.model = HuggingFaceEmbeddings(
            model_name=model_name, 
            model_kwargs=model_kwargs, 
            encode_kwargs=encode_kwargs
        )

    def vectorize(self, text: str) -> list:
        embedding = self.model.embed_query(text)
        return embedding
