from app.pipeline.document_pipeline import DocumentPipeline
from app.embeddings.embedding_pipeline import EmbeddingPipeline

# Step 1: Process the PDF
document_pipeline = DocumentPipeline()

chunks = document_pipeline.process_document(
    r"data/uploaded_pdfs/210720M-Toyota-Company-Background.pdf"
)

print(f"Chunks Created: {len(chunks)}")

# Step 2: Generate embeddings
embedding_pipeline = EmbeddingPipeline()

embedded_chunks = embedding_pipeline.process_chunks(chunks)

print(f"Embedded Chunks: {len(embedded_chunks)}")

# Display the first embedded chunk
first = embedded_chunks[0]

print("\nFirst Embedded Chunk")
print("-" * 60)
print(f"Chunk ID   : {first.chunk.chunk_id}")
print(f"Document   : {first.chunk.document_name}")
print(f"Page       : {first.chunk.page_number}")
print(f"Vector Size: {len(first.embedding)}")
print("\nText:")
print(first.chunk.text)
print("\nFirst 10 Vector Values:")
print(first.embedding[:10])