from app.ingestion.metadata import DocumentChunk


class PDFParser:
    """
    Parses a PyMuPDF document into DocumentChunk objects.
    """

    def __init__(self, document, document_name: str):
        self.document = document
        self.document_name = document_name

    def parse(self):
        """
        Extract text page by page and create DocumentChunk objects.
        """

        chunks = []

        for page_number, page in enumerate(self.document, start=1):

            text = page.get_text()

            lines = text.splitlines()

            for line_number, line in enumerate(lines, start=1):

                line = line.strip()

                if not line:
                    continue

                chunk = DocumentChunk(
                    document_name=self.document_name,
                    page_number=page_number,
                    line_start=line_number,
                    line_end=line_number,
                    text=line
                )

                chunks.append(chunk)

        return chunks