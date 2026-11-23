
from app.pipeline.document_pipeline import DocumentPipeline
from app.embeddings.embedding_pipeline import EmbeddingPipeline


def test_insert_vectors(monkeypatch):
    # Fake Qdrant manager to avoid modifying the real collection
    class MockQdrantManager:
        def __init__(self):
            self.inserted_chunks = []

        def insert_chunks(self, chunks):
            self.inserted_chunks = chunks

        def count_vectors(self):
            return len(self.inserted_chunks)

    mock_manager = MockQdrantManager()

    monkeypatch.setattr(
        "app.vectorstore.qdrant_manager.QdrantManager",
        lambda: mock_manager
    )

    # Process PDF
    document_pipeline = DocumentPipeline()

    chunks = document_pipeline.process(
        r"data/uploaded_pdfs/210720M-Toyota-Company-Background.pdf"
    )

    assert len(chunks) > 0

    # Generate embeddings
    embedding_pipeline = EmbeddingPipeline()
    embedded_chunks = embedding_pipeline.process_chunks(chunks)

    assert len(embedded_chunks) == len(chunks)

    # Insert into mocked Qdrant manager
    from app.vectorstore.qdrant_manager import QdrantManager

    manager = QdrantManager()
    manager.insert_chunks(embedded_chunks)

    # Verify insertion
    assert manager.count_vectors() == len(embedded_chunks)
