from qdrant_client import QdrantClient


class QdrantDBClient:
    """
    Creates a connection to the local Qdrant instance.
    """

    def __init__(self):
        self.client = QdrantClient(
            host="localhost",
            port=6333
        )

    def get_client(self):
        return self.client