
from app.pipeline.document_pipeline import DocumentPipeline
from app.embeddings.embedding_pipeline import EmbeddingPipeline


def test_embedding_pipeline():
    # Step 1: Process the PDF
    document_pipeline = DocumentPipeline()

    chunks = document_pipeline.process(
        r"data/uploaded_pdfs/210720M-Toyota-Company-Background.pdf"
    )

    assert len(chunks) > 0

    # Step 2: Generate embeddings
    embedding_pipeline = EmbeddingPipeline()

    embedded_chunks = embedding_pipeline.process_chunks(chunks)

    # Verify that embeddings were generated
    assert len(embedded_chunks) == len(chunks)

    first = embedded_chunks[0]

    assert first.chunk.chunk_id is not None
    assert first.chunk.document_name is not None
    assert first.chunk.page_number is not None
    assert len(first.embedding) > 0

    # Verify embedding dimensions
    assert len(first.embedding) == 384
