
from app.retrieval.hybrid_retriever import HybridRetriever

retriever = HybridRetriever()

queries = [
    "Explain Toyota's sustainability strategy",
    "Find the exact phrase Toyota Research Institute",
    "How much does Toyota invest annually in R&D?"
]

for query in queries:

    print("\n" + "=" * 75)
    print("QUERY:", query)

    results = retriever.search(query, top_k=5)

    print("SELECTED STRATEGY:",
          results[0]["retrieval_strategy"] if results else "No results")

    print("RESULT COUNT:", len(results))

    for index, result in enumerate(results, start=1):
        print(
            f"\nRank: {index} | "
            f"Page: {result['page_number']} | "
            f"Strategy: {result['retrieval_strategy']} | "
            f"Score: {result['score']:.4f}"
        )

        print("Content:", result["text"][:200])
