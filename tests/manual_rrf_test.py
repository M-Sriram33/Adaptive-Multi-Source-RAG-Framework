
from app.retrieval.fusion import ReciprocalRankFusion

# Simulated dense retrieval results
dense_results = [
    {"chunk_id": "A", "text": "Toyota research investment"},
    {"chunk_id": "B", "text": "Toyota hybrid technology"},
    {"chunk_id": "C", "text": "Toyota manufacturing"},
]

# Simulated BM25 retrieval results
bm25_results = [
    {"chunk_id": "C", "text": "Toyota manufacturing"},
    {"chunk_id": "A", "text": "Toyota research investment"},
    {"chunk_id": "D", "text": "Toyota global operations"},
]

# Initialize RRF
rrf = ReciprocalRankFusion(k=60)

# Combine rankings
fused_results = rrf.fuse(
    result_lists=[dense_results, bm25_results],
    top_k=4
)

print("\nRRF Results")
print("=" * 60)

for result in fused_results:
    print(
        f"Chunk: {result['chunk_id']} | "
        f"RRF Score: {result['rrf_score']:.6f}"
    )
