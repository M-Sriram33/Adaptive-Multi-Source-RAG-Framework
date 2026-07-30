from app.retrieval.retriever import Retriever
from app.config.settings import RETRIEVAL_SCORE_THRESHOLD


class RetrievalPipeline:
    """
    Handles document retrieval for user queries.
    """

    def __init__(self):
        self.retriever = Retriever()

    def retrieve(self, query: str, top_k: int = 5):
        """
        Retrieve the most relevant chunks and return
        them in a clean format.
        """

        results = self.retriever.search(
            query=query,
            top_k=top_k
        )

        retrieved_chunks = []

        for result in results:

            if result.score < RETRIEVAL_SCORE_THRESHOLD:
                continue

            payload = result.payload

            retrieved_chunks.append({
                "text": payload["text"],
                "document_name": payload["document_name"],
                "page_number": payload["page_number"],
                "chunk_id": payload["chunk_id"],
                "score": result.score,
            })

        return retrieved_chunks