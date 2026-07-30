from app.vectorstore.qdrant_client import QdrantDBClient

db = QdrantDBClient()

client = db.get_client()

print("Connected to Qdrant!")

print(client.get_collections())