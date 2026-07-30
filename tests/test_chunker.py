from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.parser import PDFParser
from app.chunking.chunker import DocumentChunker

loader = PDFLoader(
    r"data/uploaded_pdfs/210720M-Toyota-Company-Background.pdf"
)

document = loader.open_pdf()

parser = PDFParser(
    document,
    "210720M-Toyota-Company-Background.pdf"
)

parsed_chunks = parser.parse()

chunker = DocumentChunker(
    chunk_size=500,
    chunk_overlap=100
)

chunks = chunker.chunk(parsed_chunks)

print(f"Total chunks: {len(chunks)}")

print("\nFirst 5 chunks:\n")

for chunk in chunks[:5]:
    print("-" * 80)
    print(f"Chunk ID : {chunk.chunk_id}")
    print(f"Page     : {chunk.page_number}")
    print(f"Document : {chunk.document_name}")
    print(chunk.text)