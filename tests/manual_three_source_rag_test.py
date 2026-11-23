
from app.sources.document_source import DocumentSource
from app.sources.sql.sql_source import SQLSource
from app.sources.api.api_source import APISource

from app.router.source_router import SourceRouter
from app.pipeline.multi_source_rag_pipeline import (
    MultiSourceRAGPipeline
)


# Initialize all three data sources
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


# Initialize complete pipeline
pipeline = MultiSourceRAGPipeline(
    router=router
)


# Test 1: SQL + API
question = (
    "Compare Toyota's company background, "
    "employee salary information, and AAPL stock price."
)

result = pipeline.answer_question(question)


print("\n" + "=" * 65)
print("QUESTION:")
print(result["question"])

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES USED:")
for source in result["sources_used"]:
    print("-", source)

print("\nSOURCE REFERENCES:")
for source in result["sources"]:
    print(source)
