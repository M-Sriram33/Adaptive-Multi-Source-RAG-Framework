
import json


class ContextFusion:
    """
    Normalizes and combines retrieved information
    from multiple data sources.
    """

    def fuse(self, retrieval_output: dict) -> dict:

        context_parts = []
        sources = []

        for item in retrieval_output["results"]:

            source_type = item["source_type"]
            data = item["data"]

            # Process document results
            if source_type == "document":

                for chunk in data:

                    document_name = chunk.get(
                        "document_name", "Unknown document"
                    )

                    page_number = chunk.get(
                        "page_number", "Unknown"
                    )

                    text = chunk.get("text", "")

                    context_parts.append(
                        f"""
Source Type: Document
Document: {document_name}
Page: {page_number}
Content:
{text}
"""
                    )

                    source = {
                        "source_type": "document",
                        "document": document_name,
                        "page": page_number
                    }

                    if source not in sources:
                        sources.append(source)

            # Process SQL results
            elif source_type == "sql":

                sql_query = data.get(
                    "generated_sql", ""
                )

                sql_results = data.get(
                    "results", []
                )

                context_parts.append(
                    f"""
Source Type: SQL Database
Generated SQL:
{sql_query}

Database Results:
{json.dumps(sql_results, indent=2)}
"""
                )

                sources.append({
                    "source_type": "sql",
                    "query": sql_query,
                    "record_count": len(sql_results)
                })

            # Process API results
            elif source_type == "api":

                api_provider = data.get(
                    "api_provider", "Unknown API"
                )

                symbol = data.get(
                    "symbol", "Unknown"
                )

                api_results = data.get(
                    "results", []
                )

                context_parts.append(
                    f"""
Source Type: Financial API
API Provider: {api_provider}
Stock Symbol: {symbol}

Financial Data:
{json.dumps(api_results, indent=2)}
"""
                )

                sources.append({
                    "source_type": "api",
                    "provider": api_provider,
                    "symbol": symbol
                })

        return {
            "context": "\n".join(context_parts),
            "sources": sources,
            "source_count": len(sources)
        }
