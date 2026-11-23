from app.router.source_router import SourceRouter
from app.sources.document_source import DocumentSource


def test_source_router_selects_document_source():

    document_source = DocumentSource()

    router = SourceRouter(
        sources=[document_source]
    )

    selected_source = router.route(
        "What is the company background?"
    )

    assert selected_source is document_source
    assert selected_source.get_source_type() == "document"