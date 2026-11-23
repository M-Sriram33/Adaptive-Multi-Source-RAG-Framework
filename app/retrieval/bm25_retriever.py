
from rank_bm25 import BM25Okapi
from qdrant_client.models import ScrollRequest

from app.config.settings import QDRANT_COLLECTION_NAME
from app.vectorstore.qdrant_client import QdrantDBClient


class BM25Retriever:
    """
    Retrieves document chunks using BM25 keyword-based ranking.
    """

    def __init__(self):
        self.client = QdrantDBClient().get_client()

        self.documents = []
        self.bm25 = None

        self._build_index()

    def _build_index(self):
        """
        Fetch existing document chunks from Qdrant
        and build the BM25 index.
        """

        all_chunks = []
        offset = None

        while True:
            points, next_offset = self.client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                limit=100,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )

            all_chunks.extend(points)

            if next_offset is None:
                break

            offset = next_offset

        self.documents = [
            {
                "text": point.payload["text"],
                "document_name": point.payload["document_name"],
                "page_number": point.payload["page_number"],
                "chunk_id": point.payload["chunk_id"]
            }
            for point in all_chunks
        ]

        if not self.documents:
            raise ValueError(
                "No document chunks found in Qdrant for BM25 indexing."
            )

        tokenized_documents = [
            document["text"].lower().split()
            for document in self.documents
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    def search(self, query: str, top_k: int = 5):
        """
        Retrieve the most relevant chunks using BM25.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        results = []

        for index in ranked_indices:
            score = float(scores[index])

            # Ignore documents with no keyword relevance
            if score <= 0:
                continue

            result = self.documents[index].copy()
            result["score"] = score

            results.append(result)

            if len(results) == top_k:
                break

        return results
