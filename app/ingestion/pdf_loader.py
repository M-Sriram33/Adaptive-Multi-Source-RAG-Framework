from pathlib import Path
import fitz


class PDFLoader:
    """
    Handles loading and validating PDF documents.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def validate(self) -> bool:
        """
        Validate whether the given file exists and is a PDF.
        """

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"File not found: {self.file_path}"
            )

        if self.file_path.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        return True

    def open_pdf(self):
        """
        Open the PDF document using PyMuPDF.
        """

        self.validate()

        return fitz.open(self.file_path)

    def get_total_pages(self) -> int:
        """
        Return the total number of pages in the PDF.
        """

        document = self.open_pdf()

        return len(document)