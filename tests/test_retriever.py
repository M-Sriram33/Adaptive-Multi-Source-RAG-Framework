from app.retrieval.retriever import Retriever

retriever = Retriever()

results = retriever.search(
    "What is this document about?",
    top_k=5
)

print("=" * 60)

for i, result in enumerate(results, start=1):

    payload = result.payload

    print(f"\nResult {i}")
    print("-" * 40)
    print(f"Score : {result.score:.4f}")
    print(f"Page  : {payload['page_number']}")
    print(f"Chunk : {payload['chunk_id']}")
    print()
    print(payload["text"])