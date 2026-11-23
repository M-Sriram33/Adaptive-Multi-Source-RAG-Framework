
from app.sources.document_source import DocumentSource
from app.sources.sql.sql_source import SQLSource
from app.router.source_router import SourceRouter
from app.pipeline.multi_source_rag_pipeline import (
    MultiSourceRAGPipeline
)

# Initialize actual data sources
document_source = DocumentSource()

sql_source = SQLSource(
    database_path="data/sample_database/company.db"
)

# Register sources
router = SourceRouter(
    sources=[
        sql_source,
        document_source
    ]
)

# Initialize complete pipeline
pipeline = MultiSourceRAGPipeline(
    router=router
)

# Ask a question requiring both sources
question = (
    "Compare Toyota's company background "
    "with the employees earning more than 60000."
)

result = pipeline.answer_question(question)

print("\nQUESTION:")
print(result["question"])

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES USED:")
for source in result["sources_used"]:
    print("-", source)

print("\nSOURCE REFERENCES:")
for source in result["sources"]:
    print(source)
