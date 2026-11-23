
from app.retrieval.bm25_retriever import BM25Retriever

retriever = BM25Retriever()

query = "Toyota research development investment"

results = retriever.search(query, top_k=5)

print("\nBM25 Retrieved Chunks:", len(results))

for result in results:
    print("\nDocument:", result["document_name"])
    print("Page:", result["page_number"])
    print("BM25 Score:", result["score"])
    print("Content:", result["text"][:300])
