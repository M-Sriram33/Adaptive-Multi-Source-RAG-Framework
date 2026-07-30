from app.pipeline.document_pipeline import DocumentPipeline
from app.embeddings.embedding_pipeline import EmbeddingPipeline
from app.vectorstore.qdrant_manager import QdrantManager

PDF_PATH = r"C:\Users\dimpu\OneDrive\Desktop\adaptive-rag-framework\data\uploaded_pdfs\210720M-Toyota-Company-Background.pdf"

# Process PDF
document_pipeline = DocumentPipeline()
chunks = document_pipeline.process_document(PDF_PATH)

# Generate embeddings
embedding_pipeline = EmbeddingPipeline()
embedded_chunks = embedding_pipeline.process_chunks(chunks)

# Store in Qdrant
manager = QdrantManager()
manager.reset_collection()
manager.insert_chunks(embedded_chunks)

print(f"Total vectors stored: {manager.count_vectors()}")