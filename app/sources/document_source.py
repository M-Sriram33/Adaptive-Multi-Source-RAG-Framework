from app.sources.base_source import BaseSource
from app.pipeline.retrieval_pipeline import RetrievalPipeline


class DocumentSource(BaseSource):
    """
    Handles retrieval from indexed documents.
    """

    def __init__(self):
        self.retrieval_pipeline = RetrievalPipeline()

    def can_handle(self, query: str) -> bool:
        """
        Document source can currently handle general
        document-based questions.

        Actual intelligent routing will be added later.
        """
        return True

    def retrieve(self, query: str):
        """
        Retrieve relevant document chunks.
        """
        return self.retrieval_pipeline.retrieve(query)

    def get_source_type(self) -> str:
        return "document"