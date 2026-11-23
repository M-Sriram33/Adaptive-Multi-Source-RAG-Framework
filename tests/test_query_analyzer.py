
import pytest

from app.retrieval.query_analyzer import QueryAnalyzer


@pytest.fixture
def analyzer():
    return QueryAnalyzer()


def test_semantic_query(analyzer):
    result = analyzer.analyze("Explain Toyota's sustainability strategy")
    assert result["strategy"] == "semantic"


def test_keyword_query(analyzer):
    result = analyzer.analyze("Find the exact phrase Toyota Research Institute")
    assert result["strategy"] == "keyword"


def test_hybrid_query(analyzer):
    result = analyzer.analyze("How much does Toyota invest annually in R&D?")
    assert result["strategy"] == "hybrid"


def test_empty_query(analyzer):
    with pytest.raises(ValueError):
        analyzer.analyze("")


def test_whitespace_query(analyzer):
    with pytest.raises(ValueError):
        analyzer.analyze("   ")
