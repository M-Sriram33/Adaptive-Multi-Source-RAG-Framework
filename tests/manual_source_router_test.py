from app.router.source_router import SourceRouter

from app.sources.api.api_source import APISource
from app.sources.sql.sql_source import SQLSource
from app.sources.document_source import DocumentSource

# Initialize sources
document_source = DocumentSource()

sql_source = SQLSource(
    database_path="data/sample_database/company.db"
)

api_source = APISource()


# Register all sources
router = SourceRouter(
    sources=[
        document_source,
        sql_source,
        api_source
    ]
)


# Test queries
queries = [
    "Explain Toyota's company background",
    "Find employees earning more than 60000",
    "What is the current stock price of AAPL?",
    "Compare Toyota's background with employee salaries",
    "What is Apple's stock price according to financial data, and explain Toyota's company background?",
    "Compare AAPL stock performance with employee salary information"
]


# Test routing
for query in queries:

    print("\n" + "=" * 60)
    print("QUERY:", query)

    selected_sources = router.route_all(query)

    print(
        "SELECTED SOURCES:",
        [source.get_source_type() for source in selected_sources]
    )
