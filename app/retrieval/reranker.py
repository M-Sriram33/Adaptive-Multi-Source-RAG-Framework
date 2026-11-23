
from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    """
    Reranks retrieved document chunks using a cross-encoder.
    """

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, documents: list, top_k: int = 5):
        """
        Rerank retrieved chunks based on query-document relevance.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        if not documents:
            return []

        pairs = [
            [query, document["text"]]
            for document in documents
        ]

        scores = self.model.predict(pairs)

        reranked_documents = []

        for document, score in zip(documents, scores):
            result = document.copy()
            result["rerank_score"] = float(score)
            reranked_documents.append(result)

        reranked_documents.sort(
            key=lambda item: item["rerank_score"],
            reverse=True
        )

        return reranked_documents[:top_k]
