from app.embeddings.embedding_model import EmbeddingModel

# Initialize embedding model
embedding_model = EmbeddingModel()

# Sample text
text = "Toyota manufactures automobiles."

# Generate embedding
embedding = embedding_model.embed_text(text)

print("\nEmbedding generated successfully!")

print(f"\nEmbedding Dimension : {len(embedding)}")

print("\nFirst 10 values:")

print(embedding[:10])