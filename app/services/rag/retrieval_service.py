from app.services.rag.vector_store_service import (
    log_vector_store
)


def retrieve_similar_logs(
    query: str,
    k: int = 5
):

    results = log_vector_store.similarity_search(
        query=query,
        k=k
    )

    return results