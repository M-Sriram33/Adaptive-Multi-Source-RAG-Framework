
from app.pipeline.context_fusion import ContextFusion


def test_context_fusion_with_api():

    retrieval_output = {
        "results": [
            {
                "source_type": "api",
                "data": {
                    "api_provider": "Financial Modeling Prep",
                    "symbol": "AAPL",
                    "results": [
                        {
                            "name": "Apple Inc.",
                            "price": 352.45,
                            "change": 0.54,
                            "changePercentage": 0.15345
                        }
                    ]
                }
            }
        ]
    }

    fusion = ContextFusion()
    result = fusion.fuse(retrieval_output)

    assert "Financial API" in result["context"]
    assert "Apple Inc." in result["context"]
    assert "352.45" in result["context"]

    assert result["source_count"] == 1
    assert result["sources"][0]["source_type"] == "api"
    assert result["sources"][0]["symbol"] == "AAPL"


def test_context_fusion_with_all_sources():

    retrieval_output = {
        "results": [
            {
                "source_type": "document",
                "data": [
                    {
                        "document_name": "Toyota.pdf",
                        "page_number": 2,
                        "text": "Toyota company background."
                    }
                ]
            },
            {
                "source_type": "sql",
                "data": {
                    "generated_sql": "SELECT * FROM employees;",
                    "results": [{"name": "John", "salary": 65000}]
                }
            },
            {
                "source_type": "api",
                "data": {
                    "api_provider": "Financial Modeling Prep",
                    "symbol": "AAPL",
                    "results": [
                        {"name": "Apple Inc.", "price": 352.45}
                    ]
                }
            }
        ]
    }

    fusion = ContextFusion()
    result = fusion.fuse(retrieval_output)

    assert "Toyota company background" in result["context"]
    assert "John" in result["context"]
    assert "Apple Inc." in result["context"]

    assert result["source_count"] == 3

    source_types = [
        source["source_type"]
        for source in result["sources"]
    ]

    assert "document" in source_types
    assert "sql" in source_types
    assert "api" in source_types
