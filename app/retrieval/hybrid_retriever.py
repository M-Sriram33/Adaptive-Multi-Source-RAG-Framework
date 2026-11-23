
from app.retrieval.retriever import Retriever
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.fusion import ReciprocalRankFusion
from app.retrieval.reranker import CrossEncoderReranker
from app.retrieval.query_analyzer import QueryAnalyzer


class HybridRetriever:
    """
    Adaptive retriever supporting dense, BM25,
    and hybrid retrieval strategies.
    """

    def __init__(self):
        self.query_analyzer = QueryAnalyzer()

        # Initialize retrieval components only when needed
        self.dense_retriever = None
        self.bm25_retriever = None
        self.rrf = ReciprocalRankFusion(k=60)
        self.reranker = None

    def _get_dense_retriever(self):
        if self.dense_retriever is None:
            self.dense_retriever = Retriever()

        return self.dense_retriever

    def _get_bm25_retriever(self):
        if self.bm25_retriever is None:
            self.bm25_retriever = BM25Retriever()

        return self.bm25_retriever

    def _get_reranker(self):
        if self.reranker is None:
            self.reranker = CrossEncoderReranker()

        return self.reranker

    def _dense_search(self, query, top_k):
        points = self._get_dense_retriever().search(
            query=query,
            top_k=top_k
        )

        results = []

        for point in points:
            payload = point.payload

            results.append({
                "text": payload["text"],
                "document_name": payload["document_name"],
                "page_number": payload["page_number"],
                "chunk_id": payload["chunk_id"],
                "score": float(point.score),
                "retrieval_strategy": "semantic"
            })

        return results

    def _keyword_search(self, query, top_k):
        results = self._get_bm25_retriever().search(
            query=query,
            top_k=top_k
        )

        for result in results:
            result["retrieval_strategy"] = "keyword"

        return results

    def _hybrid_search(self, query, top_k):
        candidate_k = max(top_k * 2, 10)

        # Dense retrieval
        dense_results = self._dense_search(
            query=query,
            top_k=candidate_k
        )

        # BM25 retrieval
        bm25_results = self._get_bm25_retriever().search(
            query=query,
            top_k=candidate_k
        )

        # Reciprocal Rank Fusion
        fused_results = self.rrf.fuse(
            result_lists=[dense_results, bm25_results],
            top_k=candidate_k
        )

        # Cross-encoder reranking
        reranked_results = self._get_reranker().rerank(
            query=query,
            documents=fused_results,
            top_k=top_k
        )

        for result in reranked_results:
            result["score"] = result["rerank_score"]
            result["retrieval_strategy"] = "hybrid"

        return reranked_results

    def search(self, query: str, top_k: int = 5):
        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        # Analyze query and select strategy
        analysis = self.query_analyzer.analyze(query)
        strategy = analysis["strategy"]

        if strategy == "semantic":
            return self._dense_search(query, top_k)

        elif strategy == "keyword":
            return self._keyword_search(query, top_k)

        else:
            return self._hybrid_search(query, top_k)
