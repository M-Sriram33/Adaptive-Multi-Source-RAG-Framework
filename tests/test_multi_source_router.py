
from app.router.source_router import SourceRouter
from app.sources.base_source import BaseSource
from app.sources.sql.sql_source import SQLSource


class MockGroqClient:
    def generate(self, prompt):
        return "SELECT * FROM employees;"


class MockDocumentSource(BaseSource):
    """
    Lightweight document source for router testing.
    """

    def can_handle(self, query: str) -> bool:
        return True

    def retrieve(self, query: str):
        return {"source_type": "document"}

    def get_source_type(self) -> str:
        return "document"


def test_router_selects_sql_source():

    sql_source = SQLSource(
        database_path="data/sample_database/company.db",
        groq_client=MockGroqClient()
    )

    document_source = MockDocumentSource()

    router = SourceRouter(
        sources=[sql_source, document_source]
    )

    selected_source = router.route(
        "Show all employees"
    )

    assert selected_source.get_source_type() == "sql"


def test_router_falls_back_to_document_source():

    sql_source = SQLSource(
        database_path="data/sample_database/company.db",
        groq_client=MockGroqClient()
    )

    document_source = MockDocumentSource()

    router = SourceRouter(
        sources=[sql_source, document_source]
    )

    selected_source = router.route(
        "What is the company leave policy?"
    )

    assert selected_source.get_source_type() == "document"


def test_router_selects_multiple_sources():

    sql_source = SQLSource(
        database_path="data/sample_database/company.db",
        groq_client=MockGroqClient()
    )

    document_source = MockDocumentSource()

    router = SourceRouter(
        sources=[sql_source, document_source]
    )

    selected_sources = router.route_all(
        "Compare the company leave policy with employee leave records"
    )

    selected_types = [
        source.get_source_type()
        for source in selected_sources
    ]

    assert "sql" in selected_types
    assert "document" in selected_types
    assert len(selected_sources) == 2
