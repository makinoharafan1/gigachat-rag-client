import weaviate
from weaviate.classes.query import Filter
from typing import List, Dict

from utils.vectorizer import HFVectorizer
from utils.config import config
from entities.document_model import Document
from repositories.document_repository import DocumentRepository


class WeaviateDocumentRepository(DocumentRepository):
    def __init__(self, vectorizer: HFVectorizer):
        self.client = weaviate.connect_to_local(
            host=config.weaviate_host, port=int(config.weaviate_port)
        )
        self.collection_name = "Document_collection"
        self.vectorizer = vectorizer

    def create_collection(self):
        if self.collection_name not in self.client.collections.list_all():
            self.client.collections.create(
                name=self.collection_name,
                description="Коллекция для хранения текстовых документов",
                vectorizer_config=weaviate.classes.config.Configure.Vectorizer.none(),
                properties=[
                    weaviate.classes.config.Property(
                        name="content",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="agent_id",
                        data_type=weaviate.classes.config.DataType.TEXT
                    )
                ],
            )

    def insert_document(self, content: str, agent_id: str):
        vector = self.vectorizer.vectorize(content)
        self.client.collections.get(self.collection_name).data.insert(
            properties={
                "content": content,
                "agent_id": agent_id,
            },
            vector=vector,
        )

    def search_similar(self, query: str, agent_id: str, top_k: int = 5) -> List[Dict]:
        query_vector = self.vectorizer.vectorize(query)

        collection = self.client.collections.get(self.collection_name)
        response = collection.query.near_vector(
            near_vector=query_vector,
            filters=Filter.by_property("agent_id").equal(f"{agent_id}"),
            limit=top_k,
            return_metadata=["distance"]
        )

        results = []
        for obj in response.objects:
            result = {
                "content": obj.properties.get("content"),
                "agent_id": obj.properties.get("agent_id"),
                "distance": obj.metadata.distance 
            }
            results.append(result)

        return results
    
    def delete_collection(self):
        self.client.collections.delete(self.collection_name)

    def close(self):
        self.client.close()
