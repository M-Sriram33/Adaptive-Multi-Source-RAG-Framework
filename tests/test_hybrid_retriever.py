
from unittest.mock import MagicMock

from app.retrieval.hybrid_retriever import HybridRetriever


def test_semantic_strategy():
    retriever = HybridRetriever()

    mock_dense = MagicMock()
    mock_dense.search.return_value = []

    retriever.dense_retriever = mock_dense

    results = retriever.search(
        "Explain Toyota's sustainability strategy",
        top_k=5
    )

    mock_dense.search.assert_called_once()
    assert results == []


def test_keyword_strategy():
    retriever = HybridRetriever()

    mock_bm25 = MagicMock()
    mock_bm25.search.return_value = []

    retriever.bm25_retriever = mock_bm25

    results = retriever.search(
        "Find the exact phrase Toyota Research Institute",
        top_k=5
    )

    mock_bm25.search.assert_called_once()
    assert results == []


def test_hybrid_strategy():
    retriever = HybridRetriever()

    mock_dense = MagicMock()
    mock_dense.search.return_value = []

    mock_bm25 = MagicMock()
    mock_bm25.search.return_value = []

    mock_reranker = MagicMock()
    mock_reranker.rerank.return_value = []

    retriever.dense_retriever = mock_dense
    retriever.bm25_retriever = mock_bm25
    retriever.reranker = mock_reranker

    results = retriever.search(
        "How much does Toyota invest annually in R&D?",
        top_k=5
    )

    mock_dense.search.assert_called_once()
    mock_bm25.search.assert_called_once()
    mock_reranker.rerank.assert_called_once()
    assert results == []
