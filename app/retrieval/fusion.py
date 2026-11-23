
class ReciprocalRankFusion:
    """
    Combines ranked results from multiple retrieval methods
    using Reciprocal Rank Fusion.
    """

    def __init__(self, k=60):
        self.k = k

    def fuse(self, result_lists, top_k=5):
        scores = {}
        chunk_data = {}

        for results in result_lists:

            for rank, result in enumerate(results, start=1):

                chunk_id = result["chunk_id"]

                rrf_score = 1 / (self.k + rank)

                scores[chunk_id] = (
                    scores.get(chunk_id, 0) + rrf_score
                )

                chunk_data[chunk_id] = result

        ranked_ids = sorted(
            scores,
            key=lambda chunk_id: scores[chunk_id],
            reverse=True
        )

        fused_results = []

        for chunk_id in ranked_ids[:top_k]:

            result = chunk_data[chunk_id].copy()
            result["rrf_score"] = scores[chunk_id]

            fused_results.append(result)

        return fused_results
