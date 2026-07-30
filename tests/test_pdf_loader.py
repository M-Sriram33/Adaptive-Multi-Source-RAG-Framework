from app.ingestion.pdf_loader import PDFLoader

loader = PDFLoader(r"data/uploaded_pdfs/210720M-Toyota-Company-Background.pdf")

try:
    print("Validation:", loader.validate())
    print("Pages:", loader.get_total_pages())
except Exception as e:
    print(e)