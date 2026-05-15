from scipy.spatial.distance import (
    cosine
)


def calculate_similarity(
    current_embedding,
    historical_embeddings
):

    similarities = []

    for embedding in historical_embeddings:

        similarity = 1 - cosine(
            current_embedding,
            embedding
        )

        similarities.append(similarity)

    if not similarities:
        return 0.0

    return max(similarities)