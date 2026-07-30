from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel:
    """
    Loads and manages the embedding model.
    """

    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def embed_text(self, text: str):
        """
        Generate an embedding for a single piece of text.
        """
        return self.model.embed_query(text)

    def embed_documents(self, texts):
        """
        Generate embeddings for multiple texts.
        """
        return self.model.embed_documents(texts)