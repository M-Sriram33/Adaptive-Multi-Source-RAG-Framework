
import pytest

from app.pipeline.multi_source_rag_pipeline import (
    MultiSourceRAGPipeline
)
from app.router.source_router import SourceRouter
from app.sources.base_source import BaseSource


class MockSource(BaseSource):

    def __init__(self, source_type, response):
        self.source_type = source_type
        self.response = response

    def can_handle(self, query):
        return True

    def retrieve(self, query):
        return self.response

    def get_source_type(self):
        return self.source_type


class MockGroqClient:

    def generate(self, prompt):
        assert "Annual leave entitlement is 15 days" in prompt
        assert "Arun" in prompt

        return (
            "The annual leave entitlement is 15 days. "
            "Arun has taken 5 leave days."
        )


def test_complete_multi_source_rag_pipeline():

    document_source = MockSource(
        "document",
        [
            {
                "document_name": "leave_policy.pdf",
                "page_number": 3,
                "text": "Annual leave entitlement is 15 days."
            }
        ]
    )

    sql_source = MockSource(
        "sql",
        {
            "source_type": "sql",
            "generated_sql": "SELECT * FROM leaves;",
            "results": [
                {
                    "employee_name": "Arun",
                    "leave_days": 5
                }
            ]
        }
    )

    router = SourceRouter(
        sources=[sql_source, document_source]
    )

    pipeline = MultiSourceRAGPipeline(
        router=router,
        groq_client=MockGroqClient()
    )

    result = pipeline.answer_question(
        "Compare company leave policy with employee leave records"
    )

    assert result["answer"]
    assert "Arun" in result["answer"]

    assert "sql" in result["sources_used"]
    assert "document" in result["sources_used"]

    assert len(result["sources"]) == 2


def test_pipeline_rejects_empty_question():

    router = SourceRouter(sources=[])

    pipeline = MultiSourceRAGPipeline(
        router=router,
        groq_client=MockGroqClient()
    )

    with pytest.raises(ValueError):
        pipeline.answer_question("")
