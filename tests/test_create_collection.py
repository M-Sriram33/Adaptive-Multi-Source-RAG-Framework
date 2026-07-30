from app.vectorstore.qdrant_manager import QdrantManager

manager = QdrantManager()

manager.create_collection()

print()

print(manager.client.get_collections())