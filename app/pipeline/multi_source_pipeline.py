
from app.router.source_router import SourceRouter
from app.router.query_decomposer import QueryDecomposer


class MultiSourcePipeline:
    """
    Coordinates retrieval across multiple data sources.
    """

    def __init__(self, router: SourceRouter):
        self.router = router
        self.query_decomposer = QueryDecomposer()

    def retrieve(self, query: str) -> dict:
        """
        Retrieve information from selected sources
        using source-specific queries.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        # Step 1: Identify relevant sources
        selected_sources = self.router.route_all(query)

        source_types = [
            source.get_source_type()
            for source in selected_sources
        ]

        # Step 2: Decompose the original query
        decomposed_queries = self.query_decomposer.decompose(
            query,
            source_types
        )

        # Step 3: Retrieve using source-specific queries
        combined_results = []

        for source in selected_sources:

            source_type = source.get_source_type()
            source_query = decomposed_queries[source_type]
            print("\nSOURCE TYPE:", source_type)
            print("SOURCE QUERY:", source_query)

            result = source.retrieve(source_query)

            combined_results.append({
                "source_type": source_type,
                "query": source_query,
                "data": result
            })

        # Step 4: Return unified retrieval output
        return {
            "query": query,
            "sources_used": source_types,
            "source_count": len(selected_sources),
            "decomposed_queries": decomposed_queries,
            "results": combined_results
        }
