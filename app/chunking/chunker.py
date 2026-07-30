from collections import defaultdict
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.ingestion.metadata import DocumentChunk


class DocumentChunker:
    """
    Converts parser output into embedding-ready chunks.
    """

    def __init__(self, chunk_size=500, chunk_overlap=100):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def chunk(self, parsed_chunks):

        grouped_pages = defaultdict(list)

        # Group extracted lines page-wise
        for item in parsed_chunks:
            grouped_pages[
                (item.document_name, item.page_number)
            ].append(item)

        final_chunks = []

        chunk_id = 1

        for (document_name, page_number), lines in grouped_pages.items():

            page_text = "\n".join(
                line.text for line in lines
            )

            split_chunks = self.text_splitter.split_text(page_text)

            for text in split_chunks:

                final_chunks.append(
                    DocumentChunk(
                        document_name=document_name,
                        page_number=page_number,
                        line_start=lines[0].line_start,
                        line_end=lines[-1].line_end,
                        text=text,
                        chunk_id=chunk_id
                    )
                )

                chunk_id += 1

        return final_chunks