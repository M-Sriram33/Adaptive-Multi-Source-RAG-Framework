# ==========================
# Qdrant Configuration
# ==========================

QDRANT_COLLECTION_NAME = "documents"

EMBEDDING_DIMENSION = 384

DISTANCE_METRIC = "COSINE"


# ==========================
# Retrieval Configuration
# ==========================

TOP_K_RESULTS = 5


# ==========================
# LLM Configuration
# ==========================

LLM_MODEL = "llama-3.3-70b-versatile"

LLM_TEMPERATURE = 0.2

LLM_MAX_TOKENS = 1024

RETRIEVAL_SCORE_THRESHOLD = 0.45