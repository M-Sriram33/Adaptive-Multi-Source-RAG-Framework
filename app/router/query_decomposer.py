
from typing import Dict, List


class QueryDecomposer:
    """
    Decomposes a multi-source question into
    source-specific queries.
    """

    def decompose(
        self,
        query: str,
        source_types: List[str]
    ) -> Dict[str, str]:
        """
        Create a relevant subquery for each selected source.
        """

        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")

        normalized_query = query.lower()

        decomposed_queries = {}

        for source_type in source_types:

            if source_type == "document":

                if "toyota" in normalized_query:
                    decomposed_queries["document"] = (
                        "Retrieve Toyota company background, "
                        "history, operations and milestones."
                    )
                else:
                    decomposed_queries["document"] = query

            elif source_type == "sql":

                if any(
                    keyword in normalized_query
                    for keyword in [
                        "salary", "salaries", "employee",
                        "employees", "department"
                    ]
                ):
                    decomposed_queries["sql"] = (
                        "Retrieve relevant employee information "
                        "including employee names and salaries."
                    )
                else:
                    decomposed_queries["sql"] = query

            elif source_type == "api":

                if "aapl" in normalized_query or "apple" in normalized_query:
                    decomposed_queries["api"] = (
                        "Retrieve the stock quote for AAPL."
                    )
                else:
                    decomposed_queries["api"] = query

            else:
                decomposed_queries[source_type] = query

        return decomposed_queries
