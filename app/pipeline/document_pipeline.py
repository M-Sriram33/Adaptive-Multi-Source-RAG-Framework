from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.parser import PDFParser
from app.chunking.chunker import DocumentChunker


class DocumentPipeline:
    """
    Complete document ingestion pipeline.
    """

    def __init__(self, chunk_size=500, chunk_overlap=100):

        self.chunker = DocumentChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def process(self, file_path):

        loader = PDFLoader(file_path)

        document = loader.open_pdf()

        parser = PDFParser(
            document=document,
            document_name=loader.file_path.name
        )

        parsed_chunks = parser.parse()

        final_chunks = self.chunker.chunk(parsed_chunks)

        return final_chunks