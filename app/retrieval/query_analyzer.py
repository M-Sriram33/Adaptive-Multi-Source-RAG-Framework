
class QueryAnalyzer:
    """
    Analyzes user queries and selects a retrieval strategy.
    """

    def analyze(self, query: str) -> dict:

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        normalized_query = query.lower().strip()

        # Keywords indicating exact keyword searches
        keyword_indicators = [
            "exact phrase",
            "exact match",
            "find the phrase",
            "search for",
            "named",
            "identifier"
        ]

        # Keywords indicating broader semantic questions
        semantic_indicators = [
            "explain",
            "describe",
            "summarize",
            "what is the meaning",
            "why does",
            "how does"
        ]

        if any(
            indicator in normalized_query
            for indicator in keyword_indicators
        ):
            strategy = "keyword"

        elif any(
            indicator in normalized_query
            for indicator in semantic_indicators
        ):
            strategy = "semantic"

        else:
            strategy = "hybrid"

        return {
            "query": query,
            "strategy": strategy
        }
