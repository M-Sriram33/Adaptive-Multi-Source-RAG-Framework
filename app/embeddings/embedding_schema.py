from dataclasses import dataclass
from typing import List

from app.ingestion.metadata import DocumentChunk


@dataclass
class EmbeddedChunk:
    """
    Represents a chunk along with its embedding vector.
    """

    chunk: DocumentChunk
    embedding: List[float]