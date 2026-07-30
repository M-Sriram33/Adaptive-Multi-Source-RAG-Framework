from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentChunk:
    """
    Represents a chunk of text extracted from a document.
    """

    document_name: str
    page_number: int
    line_start: int
    line_end: int
    text: str

    chunk_id: Optional[int] = None
    source_type: str = "pdf"