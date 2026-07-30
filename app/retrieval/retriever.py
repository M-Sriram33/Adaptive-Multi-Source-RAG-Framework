from qdrant_client.models import Filter

from app.config.settings import QDRANT_COLLECTION_NAME
from app.embeddings.embedding_model import EmbeddingModel
from app.vectorstore.qdrant_client import QdrantDBClient


class Retriever:
    """
    Retrieves the most relevant document chunks from Qdrant.
    """

    def __init__(self):
        self.client = QdrantDBClient().get_client()
        self.embedding_model = EmbeddingModel()

    def search(self, query: str, top_k: int = 5):
        """
        Search Qdrant for the most relevant chunks.
        """

        query_embedding = self.embedding_model.embed_text(query)

        results = self.client.query_points(
            collection_name=QDRANT_COLLECTION_NAME,
            query=query_embedding,
            limit=top_k,
            with_payload=True,
        )

        return results.points