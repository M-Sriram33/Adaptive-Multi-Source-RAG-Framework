
from app.retrieval.hybrid_retriever import HybridRetriever
from app.retrieval.reranker import CrossEncoderReranker

# Step 1: Retrieve candidate chunks using hybrid retrieval
hybrid_retriever = HybridRetriever()

query = "How much does Toyota invest annually in research and development?"

retrieved_results = hybrid_retriever.search(
    query=query,
    top_k=10
)

print("\nHybrid Retrieval Results")
print("=" * 70)

for index, result in enumerate(retrieved_results, start=1):
    print(
        f"Rank: {index} | "
        f"Page: {result['page_number']} | "
        f"RRF Score: {result['rrf_score']:.6f}"
    )

# Step 2: Rerank retrieved chunks
reranker = CrossEncoderReranker()

reranked_results = reranker.rerank(
    query=query,
    documents=retrieved_results,
    top_k=5
)

print("\nCross-Encoder Reranked Results")
print("=" * 70)

for index, result in enumerate(reranked_results, start=1):
    print(f"\nRank: {index}")
    print(f"Document: {result['document_name']}")
    print(f"Page: {result['page_number']}")
    print(f"RRF Score: {result['rrf_score']:.6f}")
    print(f"Rerank Score: {result['rerank_score']:.6f}")
    print(f"Content: {result['text'][:300]}")
