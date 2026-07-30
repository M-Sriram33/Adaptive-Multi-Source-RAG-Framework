import uuid
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from app.config.settings import (
    QDRANT_COLLECTION_NAME,
    EMBEDDING_DIMENSION,
)

from app.vectorstore.qdrant_client import QdrantDBClient


class QdrantManager:
    """
    Handles all Qdrant operations:
    - Collection management
    - Vector insertion
    - Vector count
    """

    def __init__(self):
        self.client = QdrantDBClient().get_client()

    def collection_exists(self):
        """
        Check whether the collection already exists.
        """
        collections = self.client.get_collections().collections

        return any(
            collection.name == QDRANT_COLLECTION_NAME
            for collection in collections
        )

    def create_collection(self):
        """
        Create the collection if it doesn't already exist.
        """

        if self.collection_exists():
            print(f"Collection '{QDRANT_COLLECTION_NAME}' already exists.")
            return

        self.client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMENSION,
                distance=Distance.COSINE,
            ),
        )

        print(f"Collection '{QDRANT_COLLECTION_NAME}' created successfully.")

    def delete_collection(self):
        """
        Delete the collection if it exists.
        Useful during development to avoid duplicate vectors.
        """

        if self.collection_exists():
            self.client.delete_collection(
                collection_name=QDRANT_COLLECTION_NAME
            )
            print(f"Collection '{QDRANT_COLLECTION_NAME}' deleted.")

    def reset_collection(self):
        """
        Delete and recreate the collection.
        """

        self.delete_collection()
        self.create_collection()

    def insert_chunks(self, embedded_chunks):
        """
        Upload embedded chunks to Qdrant.
        """

        points = []

        for idx, embedded_chunk in enumerate(embedded_chunks):

            chunk = embedded_chunk.chunk

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedded_chunk.embedding,
                    payload={
                        "document_name": chunk.document_name,
                        "page_number": chunk.page_number,
                        "chunk_id": chunk.chunk_id,
                        "line_start": chunk.line_start,
                        "line_end": chunk.line_end,
                        "text": chunk.text,
                    },
                )
            )

        self.client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=points,
        )

        print(f"{len(points)} vectors inserted successfully.")

    def count_vectors(self):
        """
        Return the number of vectors stored in the collection.
        """

        result = self.client.count(
            collection_name=QDRANT_COLLECTION_NAME,
            exact=True,
        )

        return result.count