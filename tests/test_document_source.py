from app.sources.document_source import DocumentSource
from app.sources.base_source import BaseSource


def test_document_source():

    source = DocumentSource()

    assert source.get_source_type() == "document"
    assert source.can_handle("What is the company background?") is True


def test_document_source_implements_base_source():

    assert issubclass(DocumentSource, BaseSource)