from app.embeddings.embedding_model import EmbeddingModel
from app.embeddings.embedding_schema import EmbeddedChunk


class EmbeddingPipeline:
    """
    Generates embeddings for document chunks.
    """

    def __init__(self):
        self.embedding_model = EmbeddingModel()

    def process_chunks(self, document_chunks):
        """
        Convert a list of DocumentChunk objects into EmbeddedChunk objects.
        """

        texts = [chunk.text for chunk in document_chunks]

        embeddings = self.embedding_model.embed_documents(texts)

        embedded_chunks = []

        for chunk, embedding in zip(document_chunks, embeddings):
            embedded_chunks.append(
                EmbeddedChunk(
                    chunk=chunk,
                    embedding=embedding
                )
            )

        return embedded_chunks