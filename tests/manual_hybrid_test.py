
from app.retrieval.hybrid_retriever import HybridRetriever

retriever = HybridRetriever()

query = "Toyota research and development investment"

results = retriever.search(query, top_k=5)

print("\nHybrid Retrieval Results")
print("=" * 70)

for index, result in enumerate(results, start=1):
    print(f"\nRank: {index}")
    print(f"Document: {result['document_name']}")
    print(f"Page: {result['page_number']}")
    print(f"RRF Score: {result['rrf_score']:.6f}")
    print(f"Content: {result['text'][:300]}")
