from app.pipeline.document_pipeline import DocumentPipeline

pipeline = DocumentPipeline()

chunks = pipeline.process_document(
    r"data/uploaded_pdfs/210720M-Toyota-Company-Background.pdf"
)

print(f"Total Chunks: {len(chunks)}")

print()

for chunk in chunks[:5]:
    print("=" * 80)
    print(f"Chunk ID : {chunk.chunk_id}")
    print(f"Page     : {chunk.page_number}")
    print(f"Document : {chunk.document_name}")
    print(chunk.text)