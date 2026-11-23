
from app.pipeline.multi_source_pipeline import MultiSourcePipeline
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


def test_multi_source_retrieval():

    document_source = MockSource(
        "document",
        {"content": "Company leave policy information"}
    )

    sql_source = MockSource(
        "sql",
        {"employees_on_leave": 5}
    )

    router = SourceRouter(
        sources=[sql_source, document_source]
    )

    pipeline = MultiSourcePipeline(router)

    result = pipeline.retrieve(
        "Compare company leave policy with employee leave records"
    )

    assert result["source_count"] == 2

    assert "sql" in result["sources_used"]
    assert "document" in result["sources_used"]

    assert len(result["results"]) == 2


def test_multi_source_pipeline_rejects_empty_query():

    router = SourceRouter(sources=[])

    pipeline = MultiSourcePipeline(router)

    try:
        pipeline.retrieve("")
        assert False, "Empty query should be rejected"

    except ValueError:
        assert True
