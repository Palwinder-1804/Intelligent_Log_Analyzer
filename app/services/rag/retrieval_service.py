from app.services.rag.chroma_service import (
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