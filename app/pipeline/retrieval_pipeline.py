
from app.retrieval.hybrid_retriever import HybridRetriever


class RetrievalPipeline:
    """
    Handles document retrieval using hybrid search,
    RRF fusion, and cross-encoder reranking.
    """

    def __init__(self):
        self.retriever = HybridRetriever()

    def retrieve(self, query: str, top_k: int = 5):
        """
        Retrieve and rerank relevant document chunks.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        results = self.retriever.search(
            query=query,
            top_k=top_k
        )

        retrieved_chunks = []

        for result in results:
            retrieved_chunks.append({
                "text": result["text"],
                "document_name": result["document_name"],
                "page_number": result["page_number"],
                "chunk_id": result["chunk_id"],
                "score": result["score"],
            })

        return retrieved_chunks
