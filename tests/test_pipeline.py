
from app.pipeline.document_pipeline import DocumentPipeline


def test_document_pipeline():
    pipeline = DocumentPipeline()

    chunks = pipeline.process(
        r"data/uploaded_pdfs/210720M-Toyota-Company-Background.pdf"
    )

    # Verify that document processing returned chunks
    assert len(chunks) > 0

    # Verify the structure of the first chunk
    first_chunk = chunks[0]

    assert first_chunk.chunk_id is not None
    assert first_chunk.page_number is not None
    assert first_chunk.document_name is not None
    assert first_chunk.text.strip() != ""
