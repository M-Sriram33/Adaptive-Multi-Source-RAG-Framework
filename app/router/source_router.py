
from typing import List

from app.sources.base_source import BaseSource


class SourceRouter:
    """
    Routes queries to one or more appropriate data sources.
    """

    def __init__(self, sources: List[BaseSource]):
        self.sources = sources

    def route_all(self, query: str) -> List[BaseSource]:
        """
        Select appropriate sources based on the query.
        """

        normalized_query = query.lower()

        specialized_sources = [
            source for source in self.sources
            if source.get_source_type() != "document"
            and source.can_handle(query)
        ]

        document_sources = [
            source for source in self.sources
            if source.get_source_type() == "document"
        ]

        multi_source_keywords = [
            "compare",
            "comparison",
            "according to",
            "along with",
            "against",
            "difference between",
            "combined"
        ]

        document_indicators = [
            "document",
            "pdf",
            "report",
            "background",
            "company overview",
            "company profile",
            "according to the report"
        ]

        requires_multiple = any(
            keyword in normalized_query
            for keyword in multi_source_keywords
        )

        requires_documents = any(
            keyword in normalized_query
            for keyword in document_indicators
        )

        # Include documents when the query explicitly refers to document content.
        if requires_documents and document_sources:
            return specialized_sources + document_sources

        # Handle comparisons involving multiple specialized sources.
        if requires_multiple and len(specialized_sources) > 1:
            return specialized_sources

        # Handle comparisons involving one specialized source and documents.
        if requires_multiple and specialized_sources and document_sources:
            return specialized_sources + document_sources

        # Handle SQL/API-specific queries.
        if specialized_sources:
            return specialized_sources

        # Default to document retrieval.
        if document_sources:
            return document_sources

        raise ValueError("No suitable source found for the given query.")


    def route(self, query: str) -> BaseSource:

        selected_sources = self.route_all(query)

        return selected_sources[0]
