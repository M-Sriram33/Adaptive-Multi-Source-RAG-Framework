from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.parser import PDFParser

loader = PDFLoader(
    r"data/uploaded_pdfs/210720M-Toyota-Company-Background.pdf"
)

document = loader.open_pdf()

parser = PDFParser(
    document,
    "210720M-Toyota-Company-Background.pdf"
)

chunks = parser.parse()

print(f"Total chunks: {len(chunks)}")

print("\nFirst 10 chunks:\n")

for chunk in chunks[:10]:
    print(chunk)